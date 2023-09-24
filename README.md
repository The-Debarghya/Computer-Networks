# Computer Networks

- The Assignments/Projects given as a part of Computer Networks course in fifth semester curriculum of Undergraduate Course.
- This Repository contains simulation based projects of various logical link control layer protocols and actual implementation of some of the Application/Network Layer protocols as well.
- Each Assignment directory contains respective reports to know more about the particular one.

## Brief Overview:

- `Assignment 1`: Error detection methods(CRC/VRC/LRC/Checksum) in Data Link Layer simulation.
  - **How to simulate?**
  - Start `server.py` then `client.py` side by side.
- `Assignment 2`: Flow Control Methods(Stop&Wait/GoBackN/SelectiveRepeat) in Data Link Layer simulation.
  - **How to simulate?**
  - Start `channel.py` then `server.py` then `client.py` side by side.
- `Assignment 3`: Different CSMA techniques(One/Non/p-persistent) simulation.
  - **How to simulate?**
  - Create a directory named `logs` and `input`, `output` directories inside it.
  - Run `create_inputs.py` to create some input files.
  - Create `collide.txt` with text 0 in logs directory, and `log.txt`, `analysis.txt` there itself.
  - Run `main.py`.
  > - You can run the individual `one-persistent`, `p-persistent` and `non-persistent` files to simulate another type of implementation(a rather vague one).
- `Assignment 4`: CDMA technique with Walsh Code generation simulation.
  - **How to simulate?**
  - Create a directory named `logs` and `input`, `output` directories inside it.
  - Run `create_inputs.py` to create some input files.
  - Create `log.txt`, `analysis.txt` in logs directory.
  - Run `main.py`.
- `Assignment 5`: Analysis of packets using **Wireshark**.
  - **How to simulate?**
  - No simulation needed.
- `Assignment 6`: Simulation of basic networking using **Cisco Packet Tracer**.
  - **How to simulate?**
  - No simulation needed.
- `Assignment 7`: Implementation of BOOTP and DHCP.
  - **How to simulate?**
  - Both DHCP and BOOTP: Run `main.py` with help argument to get idea.
- `Assignment 8`: Implementation of FTP, DNS and Telnet.
  - **How to simulate?**
  - `FTP`: More info <a href="https://github.com/The-Debarghya/goftpd">here</a>.
  - `DNS`: Build with `go build .`, Run `minidns` binary, Test with `dig example.com @localhost -p1053`
  - `Telnet`: Start `server.py` then run `client.py`.


