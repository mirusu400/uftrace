import json

parent_map = {}
d3_data = {"name": "start", "children": []}
current_parent_map = None
fid = 0

html_template = """
<!DOCTYPE html>
<div id="container"></div>
<script src="https://cdn.jsdelivr.net/npm/d3@7"></script>

<script type="module">
const data = {{data}}
const width = 928;
const marginTop = 10;
const marginRight = 10;
const marginBottom = 10;
const marginLeft = 40;
const root = d3.hierarchy(data);
const dx = 10;
const dy = (width - marginRight - marginLeft) / (1 + root.height);

// Define the tree layout and the shape for links.
const tree = d3.tree().nodeSize([dx, dy]);
const diagonal = d3.linkHorizontal().x(d => d.y).y(d => d.x);

// Create the SVG container, a layer for the links and a layer for the nodes.
const svg = d3.create("svg")
    .attr("width", width)
    .attr("height", dx)
    .attr("viewBox", [-marginLeft, -marginTop, width, dx])
    .attr("style", "max-width: 100%; height: auto; font: 10px sans-serif; user-select: none;");

const gLink = svg.append("g")
    .attr("fill", "none")
    .attr("stroke", "#555")
    .attr("stroke-opacity", 0.4)
    .attr("stroke-width", 1.5);

const gNode = svg.append("g")
    .attr("cursor", "pointer")
    .attr("pointer-events", "all");

function update(event, source) {
  const duration = event?.altKey ? 2500 : 250; // hold the alt key to slow down the transition
  const nodes = root.descendants().reverse();
  const links = root.links();

  // Compute the new tree layout.
  tree(root);

  let left = root;
  let right = root;
  root.eachBefore(node => {
    if (node.x < left.x) left = node;
    if (node.x > right.x) right = node;
  });

  const height = right.x - left.x + marginTop + marginBottom;

  const transition = svg.transition()
      .duration(duration)
      .attr("height", height)
      .attr("viewBox", [-marginLeft, left.x - marginTop, width, height])
      .tween("resize", window.ResizeObserver ? null : () => () => svg.dispatch("toggle"));

  // Update the nodes…
  const node = gNode.selectAll("g")
    .data(nodes, d => d.id);

  // Enter any new nodes at the parent's previous position.
  const nodeEnter = node.enter().append("g")
      .attr("transform", d => `translate(${source.y0},${source.x0})`)
      .attr("fill-opacity", 0)
      .attr("stroke-opacity", 0)
      .on("click", (event, d) => {
        d.children = d.children ? null : d._children;
        update(event, d);
      });

  nodeEnter.append("circle")
      .attr("r", 2.5)
      .attr("fill", d => d._children ? "#555" : "#999")
      .attr("stroke-width", 10);

  nodeEnter.append("text")
      .attr("dy", "0.31em")
      .attr("x", d => d._children ? -6 : 6)
      .attr("text-anchor", d => d._children ? "end" : "start")
      .text(d => d.data.name)
    .clone(true).lower()
      .attr("stroke-linejoin", "round")
      .attr("stroke-width", 3)
      .attr("stroke", "white");

  // Transition nodes to their new position.
  const nodeUpdate = node.merge(nodeEnter).transition(transition)
      .attr("transform", d => `translate(${d.y},${d.x})`)
      .attr("fill-opacity", 1)
      .attr("stroke-opacity", 1);

  // Transition exiting nodes to the parent's new position.
  const nodeExit = node.exit().transition(transition).remove()
      .attr("transform", d => `translate(${source.y},${source.x})`)
      .attr("fill-opacity", 0)
      .attr("stroke-opacity", 0);

  // Update the links…
  const link = gLink.selectAll("path")
    .data(links, d => d.target.id);

  // Enter any new links at the parent's previous position.
  const linkEnter = link.enter().append("path")
      .attr("d", d => {
        const o = {x: source.x0, y: source.y0};
        return diagonal({source: o, target: o});
      });

  // Transition links to their new position.
  link.merge(linkEnter).transition(transition)
      .attr("d", diagonal);

  // Transition exiting nodes to the parent's new position.
  link.exit().transition(transition).remove()
      .attr("d", d => {
        const o = {x: source.x, y: source.y};
        return diagonal({source: o, target: o});
      });

  // Stash the old positions for transition.
  root.eachBefore(d => {
    d.x0 = d.x;
    d.y0 = d.y;
  });
}

// Do the first update to the initial configuration of the tree — where a number of nodes
// are open (arbitrarily selected as the root, plus nodes with 7 letters).
root.x0 = dy / 2;
root.y0 = 0;
root.descendants().forEach((d, i) => {
  d.id = i;
  d._children = d.children;
  if (d.depth && d.data.name.length !== 7) d.children = null;
});

update(null, root);
// Append the SVG element.
container.append(svg.node());

</script>
"""

def find_parent_map(parent_map, fid):
    for key in parent_map.keys():
        if key == fid:
            return parent_map[key]
        else:
            if parent_map[key]["_childs"]:
                find = find_parent_map(parent_map[key]["_childs"], fid)
                if find:
                    return find
    return None

def uftrace_begin(ctx):
    pass

def uftrace_entry(ctx):
    global parent_map
    global current_parent_map
    global fid

    # read arguments
    _tid = ctx["tid"]
    _depth = ctx["depth"]
    _symname = ctx["name"]
    if "args" in ctx:
        _args = ctx["args"]
    else:
        _args = []

    if _depth == 0:
        # Root depth
        new_parent_map = {
            "_fid": fid,
            "_symname": ctx["name"],
            "_depth": ctx["depth"],
            "_args": _args,
            "_childs": {}
        }
        parent_map[fid] = new_parent_map
        current_parent_map = new_parent_map

    elif _depth == current_parent_map["_depth"]:
        new_parent_map = {
            "_fid": fid,
            "_parent_fid": current_parent_map["_fid"],
            "_symname": ctx["name"],
            "_depth": ctx["depth"],
            "_args": _args,
            "_childs": {}
        }
        # Find parent map
        parent_fid = current_parent_map["_parent_fid"]
        current_parent_map = find_parent_map(parent_map, parent_fid)
        # Align new parent map into child
        current_parent_map["_childs"][fid] = new_parent_map
        current_parent_map = new_parent_map
    elif _depth > current_parent_map["_depth"]:
        # Enter a new depth
        new_parent_map = {
            "_fid": fid,
            "_parent_fid": current_parent_map["_fid"],
            "_symname": ctx["name"],
            "_depth": ctx["depth"],
            "_args": _args,
            "_childs": {}
        }
        current_parent_map["_childs"][fid] = new_parent_map
        current_parent_map = new_parent_map
    indent = _depth * 2
    space = " " * indent

    buf = " %10s [%6d] | %s%s() {" % ("", _tid, space, _symname)
    # print(buf)
    fid += 1

def uftrace_exit(ctx):
    global parent_map
    global current_parent_map
    global fid

    # read arguments
    _tid = ctx["tid"]
    _depth = ctx["depth"]
    _symname = ctx["name"]
    _duration = ctx["duration"]
    # _retval = ctx["retval"]
    if _depth != 0 and _depth < current_parent_map["_depth"]:
        parent_fid = current_parent_map["_parent_fid"]
        current_parent_map = find_parent_map(parent_map, parent_fid)

    indent = _depth * 2
    space = " " * indent
    (time, unit) = get_time_and_unit(_duration)
    buf = " %7.3f %s [%6d] | %s}" % (time, unit, _tid, space)
    buf = "%s /* %s */" % (buf, _symname)
    # print(buf)

def uftrace_end():
    global parent_map
    global d3_data
    main_fid = 0
    for key in parent_map.keys():
        if parent_map[key]["_symname"] == "main":
            main_fid = key
            break
    convert_to_d3(parent_map, d3_data, main_fid)
    html = html_template.replace("{{data}}", json.dumps(d3_data))
    with open("d3.html", "w") as f:
        f.write(html)


def convert_to_d3(parent_map, d3_data, fid):
    for key in parent_map.keys():
        if key == fid:
            if parent_map[key]["_childs"]:
                for child_key in parent_map[key]["_childs"].keys():
                    child = parent_map[key]["_childs"][child_key]
                    new_d3_data = {
                        "name": child["_symname"],
                        "children": []
                    }
                    d3_data["children"].append(new_d3_data)
                    convert_to_d3(parent_map[key]["_childs"], new_d3_data, child["_fid"])
        else:
            if parent_map[key]["_childs"]:
                convert_to_d3(parent_map[key]["_childs"], d3_data, fid)
    return None
def get_time_and_unit(duration):
    duration = float(duration)
    time_unit = ""

    if duration < 100:
        divider = 1
        time_unit = "ns"
    elif duration < 1000000:
        divider = 1000
        time_unit = "us"
    elif duration < 1000000000:
        divider = 1000000
        time_unit = "ms"
    else:
        divider = 1000000000
        time_unit = " s"

    return (duration / divider, time_unit)
