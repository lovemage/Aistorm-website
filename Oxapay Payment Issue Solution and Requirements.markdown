# Oxapay Payment Issue Solution and Requirements

## Overview
The website [www.aistorm.art](https://www.aistorm.art) uses Oxapay for USDT payments, with a Python backend deployed on Railway and a custom domain. After customers create an order, a Telegram bot notifies order creation and payment status. However, the payment window only displays a QR code without critical details such as amount, wallet address, or order number. This document provides a comprehensive analysis of the issue, step-by-step solutions, and additional requirements for the store page to be implemented by Cursor AI.

## Issue: Payment Window Lacks Detailed Information
When customers click the payment button, the popup window shows only a QR code, missing essential details like amount, wallet address, order number, and invoice ID. Below are the potential causes and detailed solutions.

### Potential Causes
1. **Oxapay API Response Incomplete or Mishandled**:
   - The Oxapay API may not return all required fields (e.g., `amount`, `address`, `orderId`).
   - The Python backend may not parse or forward these fields to the frontend.
   - The frontend may not render all available fields.
2. **Python Backend Logic Issue**:
   - The backend might only extract the QR code URL, ignoring other fields like `amount` or `address`.
   - Data passed to the frontend may be incomplete.
3. **Frontend Display Issue**:
   - The frontend template (e.g., `payment.html`) may only render the QR code, omitting other fields.
   - JavaScript or template logic may not handle all fields.
4. **Oxapay Configuration**:
   - The Oxapay merchant panel may not be configured to return full details.
   - QR code generation settings may exclude embedded details.
5. **Railway Deployment Issues**:
   - Environment variables (e.g., API key) or network issues on Railway may cause incomplete API responses.
   - Callback or return URLs may be misconfigured.
6. **Telegram Bot vs. Payment Window Data**:
   - The Telegram bot receives order data, but the payment window may use a different data processing path, leading to inconsistencies.

### Solutions
#### 1. Verify Oxapay API Response
- **Objective**: Confirm that the Oxapay API returns all required fields.
- **Steps**:
  1. Refer to Oxapay’s API documentation (available in the Oxapay merchant panel or developer portal) for the `createInvoice` endpoint.
  2. Test the API using Postman or a Python script to inspect the response.
  3. Example Python request:
     ```python
     import requests

     url = "https://api.oxapay.com/merchants/createInvoice"
     headers = {"Authorization": "Bearer YOUR_API_KEY"}
     payload = {
         "amount": 10.00,
         "currency": "USDT",
         "orderId": "your_order_id",
         "callbackUrl": "https://www.aistorm.art/callback",
         "returnUrl": "https://www.aistorm.art/success"
     }
     response = requests.post(url, json=payload, headers=headers)
     print(response.json())
     ```
  4. Expected response (example):
     ```json
     {
       "status": "success",
       "invoiceId": "INV12345",
       "amount": 10.00,
       "currency": "USDT",
       "address": "0x1234...",
       "qrCode": "https://oxapay.com/qr/INV12345.png",
       "orderId": "your_order_id"
     }
     ```
- **If Fields Are Missing**:
  - Check Oxapay merchant panel settings to ensure all fields are enabled.
  - Contact Oxapay support with your merchant ID and API request logs.
- **Logging**:
  - Add logging to capture API responses:
    ```python
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Oxapay API Response: %s", response.json())
    ```

#### 2. Inspect Python Backend Logic
- **Objective**: Ensure the backend extracts all fields from the API response and passes them to the frontend.
- **Steps**:
  1. Review the backend route handling Oxapay API responses (e.g., Flask or FastAPI).
  2. Example Flask route:
     ```python
     from flask import Flask, render_template, request
     import requests

     app = Flask(__name__)

     @app.route('/create-order', methods=['POST'])
     def create_order():
         order_data = request.form
         amount = order_data['amount']
         order_id = order_data['order_id']

         url = "https://api.oxapay.com/merchants/createInvoice"
         payload = {
             "amount": amount,
             "currency": "USDT",
             "orderId": order_id,
             "callbackUrl": "https://www.aistorm.art/callback",
             "returnUrl": "https://www.aistorm.art/success"
         }
         headers = {"Authorization": "Bearer YOUR_API_KEY"}
         response = requests.post(url, json=payload, headers=headers)
         data = response.json()

         payment_info = {
             "qr_code": data.get('qrCode'),
             "amount": data.get('amount'),
             "address": data.get('address'),
             "order_id": data.get('orderId'),
             "invoice_id": data.get('invoiceId')
         }
         return render_template('payment.html', payment_info=payment_info)
     ```
  3. Log the `data` variable to verify all fields:
     ```python
     logger.info("API Response Data: %s", data)
     ```
- **If Issue Found**:
  - Ensure `data.get()` keys match the API response structure.
  - If the response is nested (e.g., `data['payment']['amount']`), adjust the extraction logic.
  - Handle errors (e.g., check `response.status_code`).

#### 3. Validate Frontend Template
- **Objective**: Ensure the payment window displays all fields passed from the backend.
- **Steps**:
  1. Check the frontend template (e.g., `payment.html`) for rendering all fields.
  2. Example template:
     ```html
     <!DOCTYPE html>
     <html>
     <head>
         <title>USDT Payment</title>
         <style>
             body { font-family: Arial, sans-serif; text-align: center; }
             img { max-width: 200px; }
         </style>
     </head>
     <body>
         <h2>Scan QR Code for USDT Payment</h2>
         <img src="{{ payment_info.qr_code }}" alt="QR Code">
         <p><strong>Amount:</strong> {{ payment_info.amount }} USDT</p>
         <p><strong>Wallet Address:</strong> {{ payment_info.address }}</p>
         <p><strong>Order Number:</strong> {{ payment_info.order_id }}</p>
         <p><strong>Invoice ID:</strong> {{ payment_info.invoice_id }}</p>
     </body>
     </html>
     ```
  3. If using JavaScript (e.g., fetch), verify the API response:
     ```javascript
     fetch('/create-order', { method: 'POST', body: new FormData(form) })
         .then(response => response.json())
         .then(data => {
             document.getElementById('qr').src = data.qr_code;
             document.getElementById('amount').innerText = data.amount;
             document.getElementById('address').innerText = data.address;
             document.getElementById('order_id').innerText = data.order_id;
         });
     ```
- **If Issue Found**:
  - Add missing fields to the template.
  - Use browser developer tools to inspect the rendered page and verify data.

#### 4. Decode QR Code Content (Optional)
- **Objective**: Check if the QR code embeds details like wallet address.
- **Steps**:
  1. Use Python to decode the QR code:
     ```python
     from PIL import Image
     from pyzbar.pyzbar import decode
     import requests
     from io import BytesIO

     qr_url = "https://oxapay.com/qr/INV12345.png"
     response = requests.get(qr_url)
     img = Image.open(BytesIO(response.content))
     decoded = decode(img)
     if decoded:
         logger.info("QR Code Content: %s", decoded[0].data.decode('utf-8'))
     ```
  2. If the QR code contains useful data (e.g., address), display it in the frontend.
- **If Issue Found**:
  - Integrate QR code decoding into the backend and pass results to the frontend.

#### 5. Check Railway Deployment
- **Objective**: Rule out deployment-related issues.
- **Steps**:
  1. Check Railway logs for API errors:
     - Go to Railway dashboard, select your project, and view `Logs`.
     - Look for HTTP errors (e.g., 403, 404, 500) or connection issues.
  2. Verify environment variables:
     - Ensure `OXAPAY_API_KEY` is set in Railway’s `Variables` section.
     - Confirm `callbackUrl` and `returnUrl` use `https://www.aistorm.art`.
  3. Test API connectivity from Railway:
     - Deploy a test endpoint to call the Oxapay API and log the response.
- **If Issue Found**:
  - Fix environment variables or network settings.
  - Contact Railway support if connectivity issues persist.

#### 6. Compare Telegram Bot Logic
- **Objective**: Ensure the payment window uses the same data as the Telegram bot.
- **Steps**:
  1. Review the callback route handling Oxapay notifications:
     ```python
     @app.route('/callback', methods=['POST'])
     def callback():
         data = request.json
         order_id = data.get('orderId')
         amount = data.get('amount')
         status = data.get('status')
         logger.info("Callback Data: %s", data)
         send_telegram_message(f"Order {order_id} Status: {status}, Amount: {amount} USDT")
         return {"status": "ok"}, 200
     ```
  2. Store callback data in a database (e.g., SQLite) and retrieve it for the payment window.
- **If Issue Found**:
  - Align the payment window data source with the callback data.

#### 7. Contact Oxapay Support
- **Objective**: Escalate if the above steps don’t resolve the issue.
- **Steps**:
  1. Gather information:
     - Merchant ID and API key (share securely).
     - API request and response logs.
     - Description: “Payment window only shows QR code, missing amount, address, order number.”
  2. Submit a support ticket via the Oxapay merchant panel or email.

## Additional Requirements (Memo for Cursor AI)
The following requirements must be implemented on the store page:

1. **USDT Purchase Description Update**:
   - Update the description below the USDT purchase option to:  
     **"Secure payment via Oxapay, generate Order."**  
   - Note: Change "訂單" to English "Order."

2. **Store Page Navigation Bar**:
   - Add a navigation bar to the store page to improve navigation and user experience.

3. **Inline Payment Section**:
   - Add a section below the store page to display Oxapay payment details (QR code, amount, wallet address, order number, invoice ID) after clicking the payment button.
   - Avoid opening a new popup window to prevent browser blocking.
   - Example implementation:
     - Update the frontend to render a hidden `<div>` that becomes visible after payment initiation.
     - Use JavaScript to populate the `<div>` with payment details.

4. **Mobile Sticky Navigation Bar**:
   - Ensure the navigation bar remains fixed at the top of the screen when scrolling on mobile devices.
   - Example CSS:
     ```css
     nav {
         position: sticky;
         top: 0;
         z-index: 1000;
         background-color: white;
     }
     ```

5. **WeChat and Alipay Instructions**:
   - Below the "Contact Customer Service via WeChat QR Code" section, add Alipay password red packet instructions:
     **Alipay Password Red Packet Instructions**:
     1. **Open Alipay App**:  
        Ensure you are logged into your Alipay account.
     2. **Search for Password Red Packet**:  
        In the homepage search bar, enter “Password Red Packet” or navigate via [Homepage → More → Red Packet → Password Red Packet].
     3. **Send Password Red Packet**:  
        Select “Normal Red Packet” or “Lucky Red Packet.”  
        Enter the password (e.g., #AI666).  
        Set the amount and number of packets (e.g., 100 CNY for 10 packets).

## Action Plan
1. **Immediate Actions**:
   - Test Oxapay API response (Solution 1).
   - Review backend logic and log all fields (Solution 2).
   - Update frontend template to display all fields (Solution 3).
2. **Secondary Actions**:
   - Decode QR code if necessary (Solution 4).
   - Check Railway logs and environment variables (Solution 5).
   - Align Telegram bot and payment window data (Solution 6).
3. **Escalation**:
   - Contact Oxapay support with detailed logs (Solution 7).
4. **Implementation**:
   - Apply additional requirements (Memo 1–5) on the store page.
   - Test all changes on Railway and mobile devices.

## Notes
- **Logging**: Add comprehensive logging to the backend to capture API requests, responses, and errors.
- **Error Handling**: Display a warning in the payment window if fields like amount or address are missing.
- **Testing**: Test the payment flow on both desktop and mobile devices to ensure consistency.
- **Backup Plan**: If QR code issues persist, display wallet address and amount as text for manual copying.