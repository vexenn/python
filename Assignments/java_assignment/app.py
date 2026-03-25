import socket
import qrcode
from flask import Flask, render_template

app = Flask(__name__)

def show_terminal_qr(port):
    """Finds the local IP and prints a QR code to the terminal."""
    try:
        # This trick finds your 'real' local IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()

        url = f"http://{local_ip}:{port}"
        
        print("\n" + "="*30)
        print(f"SCAN TO OPEN ON YOUR PHONE:")
        print(f"URL: {url}")
        print("="*30 + "\n")
        
        qr = qrcode.QRCode()
        qr.add_data(url)
        # 'tty=True' helps it look better in some terminals
        qr.print_ascii(invert=True) 
        print("\n")
    except Exception as e:
        print(f"Could not generate QR code: {e}")

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # 1. Generate the QR code first
    show_terminal_qr(5000)
    
    # 2. Then start the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)