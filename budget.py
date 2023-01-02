class Category():

    def __init__(self, category):
        self.category = category
        self.balance = 0
        self.ledger = []

    def __str__(self) -> str:
        line = f'{self.category:*^30}' + '\n'
        ledger = self.view_ledger()
        total = 0
        for i in ledger:
            amount = str("%.2f" % i['amount']) 
            descrption = i['description']
            total += float(amount)
            l_amnt = len(amount)
            dd = descrption[:(29-l_amnt)]
            line += f'{descrption[:(29-l_amnt)]}{" "*(30-(len(dd) + l_amnt))}{amount}\n'
        line = f'{line}Total: {total}'
        return line
    
    def view_ledger(self):
        return self.ledger
    
    def get_balance(self):
        return self.balance

    def check_funds(self, check_amount):
        return self.balance >= check_amount

    def deposit(self, deposit_amount, description=''):
        self.ledger.append({'amount': deposit_amount, 'description': description})
        self.balance += deposit_amount
   
    def withdraw(self, withdraw_amount, description=''):
        if not self.check_funds(withdraw_amount):
            return False
        self.ledger.append({'amount': -withdraw_amount, 'description': description})
        self.balance -= withdraw_amount
        return True
    
    def transfer(self, transfer_amount, destination_category):
        if not self.check_funds(transfer_amount):
            return False
        self.withdraw(transfer_amount, f'Transfer to {destination_category.category}')
        destination_category.deposit(transfer_amount, f'Transfer from {self.category}')
        return True


def create_spend_chart(listofobjects):
    percentage = list()
    withdrawals = list()
    categories = list()
    spent = 0

    for object in listofobjects:
        categories.append(object.category)
        for transaction in range(0, len(object.ledger)):
            info = list(object.ledger[transaction].items())
            amount = info[0][1]
            if amount < 0:
                withdrawals.append(abs(amount))
                spent += amount

    for item in withdrawals:
        percentage.append(abs((item / spent) * 100))
    chart = ['Percentage spent by category\n']
    i = 100

    while i >= 0:
        line = [f'{str(i).rjust(3)}| ']
        for k in percentage:
            if k >= i:
                line.append('o  ')
            else:
                line.append('   ')
        line.append('\n')
        chart.append(''.join(line))
        i -= 10
    chart.append('    ')

    for _ in range(0, len(listofobjects)):
        chart.append('---')
    chart.append('-\n')
    biggest = None

    for category in categories:
        if biggest is None or len(biggest) < len(category):
            biggest = category

    for letter in range(0, len(biggest)):
        line = ['     ']
        for category in categories:
            try:
                line.append(category[letter] + '  ')
            except IndexError:
                line.append('   ')

        if letter != len(biggest) - 1:
            line.append('\n')
        joinedline = ''.join(line)
        chart.append(joinedline)

    joined_chart = ''.join(chart)

    return joined_chart
