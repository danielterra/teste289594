import sys
import starkbank
from stark_connect import connect_stark, check_environment

def transfer(to_transfer):
    if len(to_transfer) == 0:
        print("No events found to transfer")
        return 0

    amount = 0
    for invoice in to_transfer:
        amount += invoice.amount
    
    print(f"Transfering {amount} to Tony Stark")
    return starkbank.transfer.create([
        starkbank.Transfer(
            amount=amount,
            bank_code="20018183",
            branch_code="0001",
            account_number="6341320293482496",
            account_type="payment",
            tax_id="20.018.183/0001-80",
            name="Stark Bank S.A."
        )
    ])

def filter_events(events):
    to_transfer = []

    for event in events:
        if event.subscription != "invoice":
            starkbank.event.update(event.id, is_delivered=True)
            continue
        
        log = event.log
        invoice = log.invoice

        if invoice.status == "created":
            # acknowledge creation events
            starkbank.event.update(event.id, is_delivered=True)
            continue

        if invoice.status == "paid":
            # acknowledge creation events
            starkbank.event.update(event.id, is_delivered=True)
            to_transfer.append(invoice)
        
    return to_transfer

if __name__ == "__main__":
    check_environment()
    starkbank.user = connect_stark()

    events = starkbank.event.query(after="2020-03-20", is_delivered=False)
    
    to_transfer = filter_events(events)
    
    transfers_done = transfer(to_transfer)
    print(transfers_done)