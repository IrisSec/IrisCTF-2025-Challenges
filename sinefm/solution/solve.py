#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: SineFM Solve
# Author: skat
# Description: IrisCTF 2025
# GNU Radio version: 3.10.11.0

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import network
import threading



class solve(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "SineFM Solve", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("SineFM Solve")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "solve")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 192e3
        self.port = port = 6531
        self.host = host = "sinefm-f94347f3.radio.2025.irisc.tf"
        self.channel_filter = channel_filter = firdes.complex_band_pass(1.0, samp_rate, -48000, 48000, 20000, window.WIN_HAMMING, 6.76)

        ##################################################
        # Blocks
        ##################################################

        self.network_tcp_source_0 = network.tcp_source.tcp_source(itemsize=gr.sizeof_gr_complex*1,addr=host,port=port,server=False)
        self.fft_filter_xxx_0 = filter.fft_filter_ccc(2, channel_filter, 1)
        self.fft_filter_xxx_0.declare_sample_delay(0)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(0.05)
        self.audio_sink_0_0 = audio.sink(96000, '', True)
        self.analog_simple_squelch_cc_0 = analog.simple_squelch_cc((-60), 1)
        self.analog_nbfm_rx_0 = analog.nbfm_rx(
        	audio_rate=48000,
        	quad_rate=48000,
        	tau=(75e-6),
        	max_dev=5e3,
          )


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_nbfm_rx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.analog_simple_squelch_cc_0, 0), (self.analog_nbfm_rx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.audio_sink_0_0, 0))
        self.connect((self.fft_filter_xxx_0, 0), (self.analog_simple_squelch_cc_0, 0))
        self.connect((self.network_tcp_source_0, 0), (self.fft_filter_xxx_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "solve")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_channel_filter(firdes.complex_band_pass(1.0, self.samp_rate, -48000, 48000, 20000, window.WIN_HAMMING, 6.76))

    def get_port(self):
        return self.port

    def set_port(self, port):
        self.port = port

    def get_host(self):
        return self.host

    def set_host(self, host):
        self.host = host

    def get_channel_filter(self):
        return self.channel_filter

    def set_channel_filter(self, channel_filter):
        self.channel_filter = channel_filter
        self.fft_filter_xxx_0.set_taps(self.channel_filter)




def main(top_block_cls=solve, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()
    tb.flowgraph_started.set()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
