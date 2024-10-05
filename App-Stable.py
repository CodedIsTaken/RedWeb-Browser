import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')
from gi.repository import Gtk, WebKit2

class BrowserWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="RedWeb Browser")
        self.set_default_size(800, 600)

        # Create main vertical box
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.add(vbox)

        # Create horizontal box for controls
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        vbox.pack_start(hbox, False, False, 0)

        # Back button
        self.back_button = Gtk.Button.new_from_icon_name("go-previous", Gtk.IconSize.BUTTON)
        self.back_button.connect("clicked", self.go_back)
        hbox.pack_start(self.back_button, False, False, 0)

        # Forward button
        self.forward_button = Gtk.Button.new_from_icon_name("go-next", Gtk.IconSize.BUTTON)
        self.forward_button.connect("clicked", self.go_forward)
        hbox.pack_start(self.forward_button, False, False, 0)

        # Refresh button
        refresh_button = Gtk.Button.new_from_icon_name("view-refresh", Gtk.IconSize.BUTTON)
        refresh_button.connect("clicked", self.refresh)
        hbox.pack_start(refresh_button, False, False, 0)

        # URL entry
        self.url_entry = Gtk.Entry()
        self.url_entry.connect("activate", self.load_url)
        hbox.pack_start(self.url_entry, True, True, 0)

        # Create WebView
        self.webview = WebKit2.WebView()
        self.webview.connect("load-changed", self.update_buttons)
        vbox.pack_start(self.webview, True, True, 0)

        # Load a default page
        self.webview.load_uri("https://www.duckduckgo.com")
    def load_url(self, widget):
        url = self.url_entry.get_text()
        if not url.startswith(("http://", "https://")):
            url = "http://" + url
        self.webview.load_uri(url)

    def go_back(self, widget):
        self.webview.go_back()

    def go_forward(self, widget):
        self.webview.go_forward()

    def refresh(self, widget):
        self.webview.reload()

    def update_buttons(self, web_view, load_event):
        self.back_button.set_sensitive(self.webview.can_go_back())
        self.forward_button.set_sensitive(self.webview.can_go_forward())
        if load_event == WebKit2.LoadEvent.FINISHED:
            self.url_entry.set_text(self.webview.get_uri())

win = BrowserWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
