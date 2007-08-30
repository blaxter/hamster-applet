#!/usr/bin/env python
import pygtk
pygtk.require('2.0')

import os
import gtk
import gtk.glade
import gnome.ui

import hamster
import hamster.db
import time
import datetime as dt

GLADE_FILE = "add_custom_fact.glade"


class CustomFactController:
    def __init__(self, fact_date = None):
        self.wTree = gtk.glade.XML(os.path.join(hamster.SHARED_DATA_DIR, GLADE_FILE))
        self.window = self.get_widget('custom_fact_window')
        
        activities = hamster.db.get_activity_list()
        
        model = gtk.ListStore(str)
        
        for activity in activities:
          model.append((activity['name'],))
        
        self.activity_list = self.get_widget('activity')
        self.activity_list.set_model(model)
        self.activity_list.set_text_column(0)
        
        if fact_date:
            self.get_widget('activity_time').set_time(fact_date)


        self.wTree.signal_autoconnect(self)

    def get_widget(self, name):
        """ skip one variable (huh) """
        return self.wTree.get_widget(name)

    def show(self):
        self.window.show_all()

    def on_ok_clicked(self, button):
        activity = self.activity_list.get_child().get_text()
        activity_time = time.localtime(self.get_widget('activity_time').get_time())

        hamster.db.add_custom_fact(activity, activity_time)
        self.window.destroy()
        
    def on_cancel_clicked(self, button):
        self.window.destroy()
        
    def on_combo_changed(self, combo):
      # do not allow empty tasks
      activity = self.activity_list.get_child().get_text()
      self.get_widget('ok').set_sensitive(activity != '')

    
if __name__ == '__main__':
    controller = OverviewController()
    controller.show()
    gtk.main()

