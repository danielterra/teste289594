import sys
import starkbank
from stark_connect import connect_stark, check_environment

def transfer(to_transfer):
    if len(to_transfer) == 0:
        print("No events found to transfer")
        return 0

    transactions = []
    for invoice in to_transfer:
        #one transfer per transaction
        print(f"Transfering {invoice.amount} paid by {invoice.name}")

        transactions.append(
            starkbank.Transfer(
                amount=invoice.amount,
                bank_code="20018183",
                branch_code="0001",
                account_number="6341320293482496",
                account_type="payment",
                tax_id="20.018.183/0001-80",
                name="Stark Bank S.A.",
                description=f"R${invoice.amount / 100} paid by {invoice.name}"
            )
        )
    
    print(f"Transfering {len(transactions)} transactions to Tony Stark")
    return starkbank.transfer.create(transactions)

def filter_events(events):
    to_transfer = []

    for event in events:
        if event.subscription != "invoice":
            starkbank.event.update(event.id, is_delivered=True)
            continue
        
        log = event.log
        invoice = log.invoice

        if log.type == "credited":
            # acknowledge creation events
            print(f"aknowledge invoice {log.type} for {invoice.id}")
            starkbank.event.update(event.id, is_delivered=True)
            to_transfer.append(invoice)
        else:
            print(f"aknowledge invoice {log.type} for {invoice.id}")
            starkbank.event.update(event.id, is_delivered=True)
            continue
        
    return to_transfer

if __name__ == "__main__":
    check_environment()
    starkbank.user = connect_stark()

    events = starkbank.event.query(after="2020-03-20", is_delivered=True)
    event_list=list(events)
    print(f"Found {len(event_list)} events")
    print("Events", event_list)
    
    to_transfer = filter_events(event_list)
    print(f"Found {len(to_transfer)} events elegible to transfer")
    print("Invoices to transfer", to_transfer)
    
    transfers_done = transfer(to_transfer)
    print(transfers_done)