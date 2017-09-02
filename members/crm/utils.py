import base64
import pychrome


def print_pdf(url, filename=None):
    browser = pychrome.Browser(url="http://127.0.0.1:9222")

    tab = browser.new_tab()

    tab.start()
    tab.Network.enable()
    tab.Page.enable()
    tab.Page.navigate(url=url, _timeout=5)

    tab.wait(5)

    data = tab.Page.printToPDF()
    data = base64.b64decode(data['data'])

    tab.stop()
    browser.close_tab(tab)

    if filename:
        with open(filename, "wb") as fd:
            fd.write(base64.b64decode(data['data']))

        return fd

    else:
        return data
