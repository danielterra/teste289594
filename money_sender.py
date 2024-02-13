from flask import Flask, request, jsonify
import starkbank
from stark_connect import connect_stark, check_environment
from invoice_event import transfer, filter_events

app = Flask(__name__)

@app.route('/', methods=['GET'])
def heart_beat():
    return jsonify(success=True), 200

@app.route('/', methods=['POST'])
def webhook_listener():
    response_data = request.data.decode("utf-8")
    
    signature = request.headers.get('Digital-Signature')
    
    print(response_data)
    event = starkbank.event.parse(
        content=response_data,
        signature=signature,
    )
    print(event)

    if event.subscription != "invoice":
        print("event is not invoice subscription")
        return jsonify(success=True), 200
    
    # event is invoice subscription
    to_transfer = filter_events([event])
    transfer(to_transfer)

    # Return a response to StarkBank to acknowledge receipt
    return jsonify(success=True), 200

if __name__ == '__main__':
    check_environment()
    # set the user for the next calls
    starkbank.user = connect_stark()

    app.run(host='0.0.0.0', port=8080, debug=True)