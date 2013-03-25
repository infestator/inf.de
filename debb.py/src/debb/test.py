
from threading import Thread
import time
import gtk, gobject
gtk.gdk.threads_init()

class MainWindow(gtk.Window):
   def __init__(self):
       super(MainWindow, self).__init__()
       vb = gtk.VBox()
       self.add(vb)
       self.progress_bar = gtk.ProgressBar()
       vb.pack_start(self.progress_bar)
       b = gtk.Button(stock=gtk.STOCK_OK)
       vb.pack_start(b)
       b.connect('clicked', self.on_button_clicked)
       self.show_all()

   def on_button_clicked(self, button):
       self.count_in_thread(5)

   def count_in_thread(self, maximum):
       Thread(target=self.count_up, args=(maximum,)).start()

   def count_up(self, maximum):
       for i in xrange(maximum):
           fraction = (i + 1) / float(maximum)
           time.sleep(1)
           gobject.idle_add(self.set_progress_bar_fraction, fraction)

   def set_progress_bar_fraction(self, fraction):
       self.progress_bar.set_fraction(fraction)

w = MainWindow()
gtk.main()