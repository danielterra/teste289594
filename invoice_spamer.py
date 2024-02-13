# Issues 8 to 12 Invoices every 3 hours to random people for 24 hours

import sys
import starkbank
import random
import names
from cpf_generator import CPF
from stark_connect import check_environment, connect_stark

def generate_invoices(iterations:int):
    invoices=[]
    for i in range(iterations+1):
        invoices.append(
            starkbank.Invoice(
                amount=random.randint(1000, 100000),
                name=names.get_full_name(),
                tax_id=CPF.generate().format(),
            )
        )

    try:
        created_invoices = starkbank.invoice.create(invoices)
    except starkbank.error.InputErrors as exception:
        for error in exception.errors:
            print(f"ERROR S5 {error.code}: {error.message}")
            sys.exit(5)
    except starkbank.error.InternalServerError as exception:
        for error in exception.errors:
            print(f"ERROR S6 {error.code}: {error.message}")
            sys.exit(6)
    except starkbank.error.UnknownError as exception:
        for error in exception.errors:
            print(f"ERROR S7 {error.code}: {error.message}")
            sys.exit(7)

    for invoice in created_invoices:
        print("\n\n\nInvoice created")
        print(invoice)

if __name__ == "__main__":
    check_environment()
    # set the user for the next calls
    starkbank.user = connect_stark()
    generate_invoices(8)