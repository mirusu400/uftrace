% UFTRACE(1) Uftrace User Manuals
% Namhyung Kim <namhyung@gmail.com>
% Sep, 2018

이름
====
uftrace - 프로그램 함수 호출 분석 도구


사용법
======
uftrace [*record*|*replay*|*live*|*report*|*info*|*dump*|*recv*|*graph*|*script*|*tui*] [*options*] COMMAND [*command-options*]


설명
====
uftrace 는 `COMMAND` 에 주어지는 프로그램의 실행을 함수 단위로 추적(trace)하는
분석 도구이다.  `COMMAND` 에 주어지는 프로그램은 `-pg` 또는 `-finstrument-function`
로 컴파일된 C 또는 C++ 프로그램이어야 한다.
COMMAND 의 대상이 되는 실행 이미지는 이름을 읽을 수 있도록
(i.e `strip`(1) 되어 있지 않은) ELF 심볼 테이블을 필요로 한다.

uftrace 는 `git`(1) 또는 `perf`(1) 와 같은 방식으로 다수의 보조 명령어들을 갖는다.
아래에 보조 명령어과 함께 간략한 설명이 있다.  더 자세한 정보를 위해서는 각 보조
명령어들의 메뉴얼 페이지를 참조할 수 있다.  또한, 이 페이지에 있는 옵션들은 다른
보조 명령어들과 함께 사용될 수 있다.

만약 보조 명령어를 명시적으로 입력하지 않으면, uftrace 는 `record` 와 `replay` 를
한번에 수행하는 `live` 보조 명령어로 동작한다.
live 명령어의 옵션들은 `uftrace-live`(1) 에서 참조할 수 있다.
더 자세한 분석을 위해, `uftrace-record`(1) 를 통해 데이터를 기록하고,
`uftrace-replay`(1), `uftrace-report`(1), `uftrace-info`(1), `uftrace-dump`(1),
`uftrace-script`(1), `uftrace-tui`(1) 중 하나를 사용하여 분석할 수 있다.


보조 명령어
============
record
:   주어진 명령어를 실행하고 데이터를 파일이나 디렉터리에 저장한다.

replay
:   저장된 함수를 시간 정보와 함께 출력한다.

live
:   실시간 추적을 진행하고, 실행되는 함수를 출력한다.

report
:   다양한 통계와 저장된 데이터를 요약하여 출력한다.

info
:   OS 버전, CPU 정보, 라인 수 등의 추가적인 정보를 출력한다.

dump
:   데이터 파일에 있는 저수준 데이터를 출력한다.

recv
:   네트워크로부터 전달받은 데이터를 저장한다.

graph
:   함수 호출 그래프를 출력한다.

script
:   저장된 함수 추적 데이터와 관련된 스크립트를 실행한다.

tui
:   graph 와 report 를 볼 수 있는 텍스트 형식의 사용자 인터페이스를 보여준다.


옵션
====
-h, \--help
:   사용법을 옵션 리스트로 설명과 함께 출력한다.

\--usage
:   사용법을 문자열로 출력한다.

-V, \--version
:   프로그램의 버전을 출력한다.

-v, \--verbose
:   세부적인 메시지를 출력한다.  이 옵션은 디버그 레벨을 3 까지 올릴 수 있다.

\--debug
:   디버그 메시지를 출력한다.  이 옵션은 `-v`/`--verbose` 와 같으며 하위 호환성을
    위해서만 존재한다.

\--debug-domain=*DOMAIN*[,*DOMAIN*, ...]
:   디버그 메시지 출력을 도메인으로 한정한다. 가능한 도메인들은 uftrace, symbol,
    demangle, filter, fstack, session, kernel, mcount, dynamic, event, script
    그리고 dwarf 가 있다.
    위의 도메인들은 콜론을 이용해 선택적으로 각각의 도메인 레벨을 지정할 수 있다.
    예를 들어, `-v --debug-domain=filter:2` 는 filter 옵션에 디버깅 레벨을 지정하고,
    다른 도메인은 디버그 레벨을 1로 지정한다.

-d *DATA*, \--data=*DATA*
:   데이터를 저장할 디렉터리의 이름을 정한다.  기본값은 `uftrace.data` 이다.

\--logfile=*FILE*
:   경고와 디버그 메시지를 stderr 을 대신해 *FILE* 안에 저장한다.

\--color=*VAL*
:   결과에 색을 지정하거나 지정하지 않는다. 가능한 값은
    "yes"(= "true" | "1" | "on" ), "no"(= "false" | "0" | "off" ) 와 "auto" 이다.
    "auto" 는 출력이 터미널인 경우 기본적으로 색을 지정한다.

\--no-pager
:   pager 기능을 사용하지 않는다.

\--opt-file=*FILE*
:   uftrace 실행에 사용하는 옵션을 파일에서 읽어서 적용한다.


보조 명령별 옵션
================
이 옵션들은 완전성을 위해 여기에 존재하지만, 특정 보조 명령어에서만
유효하다.

uftrace-<*subcommand*> 메뉴얼 페이지에서 추가적인 정보를 확인할 수 있다.
*uftrace-live*(1) 메뉴얼 페이지는 특이한 페이지이다: 보조 멍령어 `live` 는
`record` 와 `replay` 의 기능을 내부적으로 진행한다.  그러므로,


\--avg-self
:   각 함수의 자체 시간(self time)의 평균, 최소, 최대 시간을 보여준다.

\--avg-total
:   각 함수의 총 시간(total time)의 평균, 최소, 최대 시간을 보여준다.

-a, \--auto-args
:   알려진 함수의 인자와 반환값들을 자동으로 기록한다.

-A, \--argument=*FUNC*@arg[,arg,...]
:   함수 인자를 표시한다.

-b, \--buffer=*SIZE*
:   저장할 데이터의 내부 버퍼 크기를 설정한다.  기본 사이즈는 128k 이다.

\--chrome
:   구글 크롬 추적 기능에서 사용되는 JSON 형식의 결과물을 표시한다.

\--clock
:   타임스탬프를 읽는 클럭 소스를 설정한다.  기본 설정은 'mono' 이다.

\--column-offset=*DEPTH*
:   각 열의 간격(offset) 크기를 명시한다.  기본 간격은 8 이다.

\--column-view
:   열(column) 별로 분리하여 각각의 태스크를 출력한다.

-C, \--caller-filter=*FUNC*
:   Only trace callers of those FUNCs

\--demangle=*TYPE*
:   C++ symbol demangling: full, simple, no
:   (default: simple)

\--diff=*DATA*
:   Report differences

\--diff-policy=*POLICY*
:   Control diff report policy
:   (default: 'abs,compact,no-percent')

\--disable
:   Start with tracing disabled

-D, \--depth=*DEPTH*
:   Trace functions within *DEPTH*

-e, \--estimate-return
:   Use only entry record type for safety

\--event-full
:   Show all events outside of function

-E, \--Event=*EVENT*
:   Enable *EVENT* to save more information

\--flame-graph
:   Dump recorded data in FlameGraph format

\--flat
:   Use flat output format

\--force
:   Trace even if executable is not instrumented

\--format=*FORMAT*
:   Use *FORMAT* for output: normal, html (default: normal)

-f, \--output-fields=*FIELD*
:   Show FIELDs in the replay or graph output

-F, \--filter=*FUNC*
:   Only trace those FUNCs

-g, \--agent
:   Start an agent in mcount to listen to commands

\--graphviz
:   Dump recorded data in *DOT* format

-H, \--hide=*FUNC*
:   Hide FUNCs from trace

\--host=*HOST*
:   Send trace data to *HOST* instead of write to file

-k, \--kernel
:   Trace kernel functions also (if supported)

\--keep-pid
:   Keep same pid during execution of traced program

\--kernel-buffer=*SIZE*
:   Size of kernel tracing buffer (default: 1408K)

\--kernel-full
:   Show kernel functions outside of user

\--kernel-only
:   Dump kernel data only

\--kernel-skip-out
:   Skip kernel functions outside of user (deprecated)

-K, \--kernel-depth=*DEPTH*
:   Trace kernel functions within *DEPTH*

\--libmcount-single
:   Use single thread version of libmcount

\--list-event
:   List available events

\--logfile=*FILE*
:   Save warning and debug messages into this file instead of stderr.

-l, \--nest-libcall
:   Show nested library calls

\--libname
:   Show libname name with symbol name

\--libmcount-path=*PATH*
:   Load libmcount libraries from this *PATH*

\--match=*TYPE*
:   Support pattern match: regex, glob (default:
:   regex)

\--max-stack=*DEPTH*
:   Set max stack depth to *DEPTH* (default: 65535)

\--no-args
:   Do not show arguments and return value

\--no-comment
:   Don't show comments of returned functions

\--no-event
:   Disable (default) events

\--no-sched
:   Disable schedule events

\--no-sched-preempt
:   Hide pre-emptive schedule event
:   but show regular(sleeping) schedule event

\--no-libcall
:   Don't trace library function calls

\--no-merge
:   Don't merge leaf functions

\--no-pltbind
:   Do not bind dynamic symbols (*LD_BIND_NOT*)

\--no-randomize-addr
:   Disable *ASLR* (Address Space Layout Randomization)

\--nop
:   No operation (for performance test)

\--num-thread=*NUM*
:   Create *NUM* recorder threads

-N, \--notrace=*FUNC*
:   Don't trace those FUNCs

-p, \--pid=*PID*
:   Connect to the *PID* of an interactive mcount instance

\--port=*PORT*
:   Use *PORT* for network connection (default: 8090)

-P, \--patch=*FUNC*
:   Apply dynamic patching for FUNCs

\--record
:   Record a new trace before running given script

\--report
:   Show a live report before replay

\--rt-prio=*PRIO*
:   Record with real-time (*FIFO*) priority

-r, \--time-range=*TIME*~*TIME* Show output within the *TIME*(timestamp or elapsed time)
:   range only

\--run-cmd=*CMDLINE*
:   Command line that want to execute after tracing
:   data received

-R, \--retval=*FUNC*[@retspec]
:   Show function return values for *FUNC*, optionally with given uftrace retspec

\--sample-time=*TIME*
:   Show flame graph with this sampling time

\--signal=*SIGNAL*@act[,act,...]
:   Trigger the given actions when the given *SIGNAL* is received

\--sort-column=*INDEX*
:   Sort diff report on column *INDEX* (default: 2)

\--srcline
:   Enable recording source line info

\--symbols
:   Print symbol table instead of the recorded tracing info

-s, \--sort=*KEY*[,*KEY*,...]
:   Sort reported functions by KEYs (default: 2)

-S, \--script=*SCRIPT*
:   Run a given *SCRIPT* in function entry and exit

-t, \--time-filter=*TIME*
:   Hide small functions run less than the *TIME*

\--task
:   [info]: Print task relationship in a tree form instead of the tracing info.

\--task-newline
:   Interleave a newline when task is changed

\--tid=*TID*[,*TID*,...]
:   Only replay those tasks

\--time
:   Print time information

-T, \--trigger=*FUNC*@act[,act,...]
:   Trigger action on those FUNCs

-U, \--unpatch=*FUNC*
:   Don't apply dynamic patching for FUNCs

\--with-syms=*DIR*
:   Use symbol files in the *DIR*

-W, \--watch=*POINT*
:   Watch and report *POINT* if it's changed

-Z, \--size-filter=*SIZE*
:   Apply dynamic patching for functions bigger than *SIZE*

For more detail about these command-specific options,
please see the more specific manual pages listed below.


함께 보기
========
`uftrace-live`(1), `uftrace-record`(1), `uftrace-replay`(1), `uftrace-report`(1), `uftrace-info`(1), `uftrace-dump`(1), `uftrace-recv`(1), `uftrace-graph`(1), `uftrace-script`(1), `uftrace-tui`(1)


번역자
======
류준호 <ruujoon93@gmail.com>, 김성진 <mirusu400@naver.com>
