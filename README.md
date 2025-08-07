# SnapSpend

SnapSpend is a Flask-based web application that allows users to register, log in, upload invoice images, and extract structured financial data using OCR and AI. It is deployed using Docker with HAProxy load balancing between two Flask backend servers.

# Demo Video

# Watch the Demo:

Click here to view SnapSpend in action
(Replace this link with your actual video URL)

# How to Run This Project (Step by Step)

1. Clone the Project
   bash
   Copy
   Edit
   git clone https://github.com/your-username/SnapSpend.git
   cd SnapSpend
2. Build and Run the Docker Containers
   bash
   Copy
   Edit
   docker-compose up --build
   This command will:

Build your Flask app image

Start two backend servers: web-01 and web-02

Launch lb-01 (load balancer) on port 8080

3. Access the App in Your Browser
   Visit:

arduino
Copy
Edit
http://localhost:8080
Refresh multiple times — requests will alternate between web-01 and web-02.

You can also check which server served the request:

bash
Copy
Edit
curl -I http://localhost:8080
Check the X-Served-By response header.

# Troubleshooting: Load Balancer lb-01 Not Working?

If you're getting errors from lb-01, follow these steps:

Step-by-Step Fix
bash
Copy
Edit
docker exec -it lb-01 bash
apt update
apt install vim
vim /etc/haproxy/haproxy.cfg
Paste this configuration:

pgsql
Copy
Edit
global
daemon
maxconn 256

defaults
mode http
timeout connect 5000ms
timeout client 50000ms
timeout server 50000ms
option redispatch
retries 3

frontend http-in
bind \*:80
default_backend flask_servers

backend flask_servers
balance roundrobin
option httpchk GET /
http-response set-header X-Served-By %[srv_name]
server web-01 web-01:8000 check inter 2s rise 3 fall 3
server web-02 web-02:8000 check inter 2s rise 3 fall 3
Then restart HAProxy:

bash
Copy
Edit
service haproxy restart

# Future Improvements

- Add HTTPS support

- Visual dashboard for financial insights

- AI-powered analytics using large language models to:

1.  Summarize spending patterns

2.  Offer financial advice

- Role-based access (admin/user)

- Advanced notifications & alerts

# APIs Used & Credits

OCR API → OCR - RapidAPI

AI Extraction → Gemini Pro (Google Generative AI)

Database & Auth → Supabase

# Author

MUGISHA Jonathan
