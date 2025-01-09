FROM ghcr.io/gem5/ubuntu-24.04_all-dependencies:v24-0
COPY build/X86/gem5.opt /
COPY challenge/ /challenge/
COPY configs /
CMD ["/gem5.opt", "/challenge/challenge.py"]
