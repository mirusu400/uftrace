import json
import sys

filename = "d3.html"
d3_data = {"name": "start", "children": [], "fid": -1}
parent_map = {}
current_parent_map = None
fid = 0

html_template = """

<!DOCTYPE html>
<script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
<script src="https://code.jquery.com/jquery-3.6.0.min.js" integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=" crossorigin="anonymous"></script>
<style>
.tooltip-box {
	background: rgba(0, 0, 0, 0.7);
	visibility: hidden;
	position: absolute;
	border-style: solid;
  border-width: 1px;
  border-color: black;
  border-top-right-radius: 0.5em;
}
.tooltip-box-text {
  visibility: hidden;
  position: absolute;
  font-size: 9px;
}
</style>

<div id="container">
  <ct-visualization id="tree-container"allowfullscreen ></ct-visualization>
</div>
<script type="module">
const data = {{data}}
const width = 960;
const marginTop = 100;
const marginRight = 10;
const marginBottom = 10;
const marginLeft = 150;
const tooltipWidth = 100;
const tooltipHeight = 50;
const root = d3.hierarchy(data);
const dx = 150;
const dy = 150;

// Define the tree layout and the shape for links.
const tree = d3.tree().nodeSize([dx, dy]);
const diagonal = d3.linkHorizontal().x(d => d.y).y(d => d.x);

// Create the SVG container, a layer for the links and a layer for the nodes.
const svg = d3.create("svg")
    .attr("preserveAspectRatio", "xMinYMin meet")
    // .attr("viewBox", "0 0 960 500")

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
  let top = root;
  let bottom = root;
  root.eachBefore(node => {
    if (node.x < left.x) left = node;
    if (node.x > right.x) right = node;
    if (node.y < top.y) top = node;
    if (node.y > bottom.y) bottom = node;
  });

  const height = right.x - left.x + marginTop + marginBottom + 100;
  const width = bottom.y - top.y + marginLeft + marginRight + 100;


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
      .attr("node-id", d => d.id)
      .attr("transform", d => `translate(${source.y0},${source.x0})`)
      .attr("fill-opacity", 0)
      .attr("stroke-opacity", 0)
      .attr("width", 70)
      .attr("height", 50)
      .on('mouseover', function(d) {
        // Get node-id
        const nodeId = $(this).attr('node-id');
        $('#nodeInfoID' + nodeId).css('visibility', 'visible');
        $('#nodeInfoTextID' + nodeId).css('visibility', 'visible');
      })
      .on('mouseout', function(d) {
        const nodeId = $(this).attr('node-id');
        $('#nodeInfoID' + nodeId).css('visibility', 'hidden');
        $('#nodeInfoTextID' + nodeId).css('visibility', 'hidden');
      });


  const nodeRect = nodeEnter.append("rect")
      .attr("node-rect-id", d => d.id)
      .attr("id", d => 'nodeRectID' + d.id)
      .attr("width", 70)
      .attr("height", 50)
      .attr("fill", "#ddd")
      .attr("stroke", "#555")
      .attr("stroke-width", 1)
      .attr("rx", 7)
      .attr("y", "-25")
      .attr("x", "-70")

      .on("click", (event, d) => {
        d.children = d.children ? null : d._children;
        update(event, d);
      });

  const nodeCircle = nodeEnter.append("circle")
      .attr("r", 2.5)
      .attr("fill", d => d._children ? "#555" : "#999")
      .attr("stroke-width", 10)
      .on("click", (event, d) => {
        d.children = d.children ? null : d._children;
        update(event, d);
      });

  const nodeText = nodeEnter.append("text")
      .attr("dy", "0.31em")
      .attr("x", -6)
      .attr("text-anchor", "end")
      .text(d => d.data.name)
      .clone(true).lower()
      .attr("stroke-linejoin", "round")
      .attr("stroke-width", 3)
      .attr("stroke", "white")
      .on("click", (event, d) => {
        d.children = d.children ? null : d._children;
        update(event, d);
      });

  const nodeToolTipBox = nodeEnter.append("rect")
		.attr('id', function(d) { return 'nodeInfoID' + d.id; })
    .attr('x', -(tooltipWidth / 3))
		.attr('y', -5)
		.attr('width', tooltipWidth)
		.attr('height', tooltipHeight)
    .attr('class', 'tooltip-box')
    .attr('rx', 5)
    .style('fill-opacity', 0.8)
    .on("click", (event, d) => {
      const mouseX = event.pageX;
      const mouseY = event.pageY;
      const nodeRect = $('#nodeRectID' + d.id);
      const nodeRectX1 = nodeRect.offset().left;
      const nodeRectY1 = nodeRect.offset().top;
      const nodeRectX2 = nodeRectX1 + nodeRect.width();
      const nodeRectY2 = nodeRectY1 + nodeRect.height();
      if (mouseX < nodeRectX1 || mouseX > nodeRectX2 || mouseY < nodeRectY1 || mouseY > nodeRectY2) {
        return;
      }
      // If mouse is on nodeRect
      d.children = d.children ? null : d._children;
      update(event, d);
    })
    .on("mousemove", (event, d) => {
      const mouseX = event.pageX;
      const mouseY = event.pageY;
      const nodeRect = $('#nodeRectID' + d.id);
      const nodeRectX1 = nodeRect.offset().left;
      const nodeRectY1 = nodeRect.offset().top;
      const nodeRectX2 = nodeRectX1 + nodeRect.width();
      const nodeRectY2 = nodeRectY1 + nodeRect.height();
      if (mouseX < nodeRectX1 || mouseX > nodeRectX2 || mouseY < nodeRectY1 || mouseY > nodeRectY2) {
        $('#nodeInfoID' + d.id).css('visibility', 'hidden');
        $('#nodeInfoTextID' + d.id).css('visibility', 'hidden');
      } else {
        $('#nodeInfoID' + d.id).css('visibility', 'visible');
        $('#nodeInfoTextID' + d.id).css('visibility', 'visible');
      }
    })

  const nodeToolTipText = nodeEnter.append("text")
    .attr('id', function(d) { return 'nodeInfoTextID' + d.id; })
    .attr('x', -(tooltipWidth / 3) + 10)
		.attr('y', 15)
		.attr('width', tooltipWidth - 30)
		.attr('height', tooltipHeight)
    .attr('class', 'tooltip-box-text')
    .style("fill", "white")
    .append("tspan")
    .text(d => {
      if (!d.data.args) {
        return `args: None`;
      }
      return `args  : ${d.data.args}`;
    })
    .append("tspan")
    .attr("x", -(tooltipWidth / 3) + 10)
    .attr("dy", "1.5em")
    .text(d => {
      if (!d.data.depth) {
        return `depth: None`;
      }
      return `depth: ${d.data.depth}`;
    })


  const nodeUpdate = node.merge(nodeEnter).transition(transition)
      .attr("transform", d => `translate(${d.y},${d.x})`)
      .attr("fill-opacity", 1)
      .attr("stroke-opacity", 1);

  const nodeExit = node.exit().transition(transition).remove()
      .attr("transform", d => `translate(${source.y},${source.x})`)
      .attr("fill-opacity", 0)
      .attr("stroke-opacity", 0);

  const link = gLink.selectAll("path")
    .data(links, d => d.target.id);

  const linkEnter = link.enter().append("path")
      .attr("d", d => {
        const o = {x: source.x0, y: source.y0};
        return diagonal({source: o, target: o});
      });

  link.merge(linkEnter).transition(transition)
      .attr("d", diagonal);

  link.exit().transition(transition).remove()
      .attr("d", d => {
        const o = {x: source.x, y: source.y};
        return diagonal({source: o, target: o});
      });

  root.eachBefore(d => {
    d.x0 = d.x;
    d.y0 = d.y;
  });
}

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
    _depth = ctx["depth"]
    if "args" in ctx:
        _args = ctx["args"]
    else:
        _args = []

    if _depth == 0:
        # If root node
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
        # If same depth, just add to current parent map
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
    fid += 1

def uftrace_exit(ctx):
    global parent_map
    global current_parent_map
    global fid

    _depth = ctx["depth"]

    if _depth != 0 and _depth < current_parent_map["_depth"]:
        parent_fid = current_parent_map["_parent_fid"]
        current_parent_map = find_parent_map(parent_map, parent_fid)

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
    with open(filename, "w") as f:
        f.write(html)


def convert_to_d3(parent_map, d3_data, fid):
    for key in parent_map.keys():
        if key == fid:
            if parent_map[key]["_childs"]:
                for child_key in parent_map[key]["_childs"].keys():
                    child = parent_map[key]["_childs"][child_key]
                    new_d3_data = {
                        "name": child["_symname"],
                        "args": child["_args"],
                        "fid": child["_fid"],
                        "depth": child["_depth"],
                        "children": []
                    }
                    d3_data["children"].append(new_d3_data)
                    convert_to_d3(parent_map[key]["_childs"], new_d3_data, child["_fid"])
        else:
            if parent_map[key]["_childs"]:
                convert_to_d3(parent_map[key]["_childs"], d3_data, fid)
    return None
