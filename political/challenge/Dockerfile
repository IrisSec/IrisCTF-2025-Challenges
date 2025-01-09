# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
FROM python:3.12 as chroot

RUN /usr/sbin/useradd -u 1000 user

RUN python3 -m pip install flask waitress 
RUN apt-get update
RUN apt-get install -y socat

COPY chal.py /home/user/
COPY run.sh /home/user/
COPY index.html /home/user/

FROM gcr.io/kctf-docker/challenge@sha256:0f7d757bcda470c3bbc063606335b915e03795d72ba1d8fdb6f0f9ff3757364f

COPY --from=chroot / /chroot

COPY nsjail.cfg /home/user/

CMD kctf_setup && kctf_drop_privs nsjail --config /home/user/nsjail.cfg -- /home/user/run.sh
