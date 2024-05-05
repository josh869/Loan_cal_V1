from data_dict import master_dict

class Loan_cal:

    global master_dict

    interest = 0.0375

    def __init__(self, state, net_pay, repayment, balance, accrude_interest, specific_deduction,
                 specific_loan_amt):
        self.state = state
        self.netpay = net_pay
        self.repayment = repayment
        self.balance = balance
        self.accrude_interest = accrude_interest
        self.specific_deduction = specific_deduction
        self.specific_loan_amt = specific_loan_amt

    def confirm_inputs(self):

        dell = []
        new_cont = []
        input_list = [self.netpay, self.repayment, self.accrude_interest, self.balance,
                      self.specific_deduction, self.specific_loan_amt]
        for inputs in input_list:
            new_num = []

            if '.' in inputs:
                inputs = inputs[:inputs.find('.')]
            else:
                pass

            for values in inputs:
                try:
                    values = int(values)
                    new_num.append(values)
                except:
                    dell.append(values)

            nv = ''
            for i in new_num:
                nv = nv + str(i)
            try:
                new_cont.append(int(nv))
            except:
                print('Invalid numeric input')

        print(new_cont)
        print('')

        self.netpay, self.repayment, self.accrude_interest, self.balance, self.specific_deduction, self.specific_loan_amt = [
            new_cont[i] for i in range(len(new_cont))]

        print(
            f'netpay:{self.netpay}   Repayment:{self.repayment}   Acc_interest:{self.accrude_interest}  Pri_balance:{self.balance}   Specific_deduction:{self.specific_deduction}   Specific_loan_amt:{self.specific_loan_amt}')
        print('')

    def interest_confirmation(self):
        if self.state in ['state2', 'state3', 'state5', 'state1', 'state4', 'state7', 'state8', 'state6']:
            Loan_cal.interest = 0.0375
        else:
            Loan_cal.interest = 0.035

        print('interest confirmed ')

    def calculate_loan_amt(self, dtir, tenure):
        total_netpay = self.netpay + self.repayment
        netpay_loan_amt = round(((total_netpay * dtir * tenure) / (1 + (Loan_cal.interest * tenure))), -3) - 1000
        return netpay_loan_amt

    @staticmethod
    def calculate_monthly_deduction(md_loan_amt, tenure):
        return round((1 + (Loan_cal.interest * tenure)) * (md_loan_amt / tenure), 1)

    def outstanding_balance(self):
        return self.accrude_interest + self.balance

    def calculate_admin_fee(self, adf_loan_amt):
        return round((2 / 100 * (adf_loan_amt - self.outstanding_balance())), 2)

    def calculate_eligible_loan_amount(self, eli_loan_amt, admin_fee):
        return (eli_loan_amt - self.outstanding_balance()) - admin_fee

    @staticmethod
    def calculate_specific_deduction(specific_deduction, tenure):
        one = specific_deduction * tenure
        two = 1 + (Loan_cal.interest * tenure)
        return one / two

    def netpay_loan_cal(self, specific_deduction, specific_loan_amt):
        lt_cont = []
        output_values = []

        for val in Loan_cal.master_dict:
            if self.state == val:
                print('valid state entered')
                new_dict = Loan_cal.master_dict[self.state]

                for values in new_dict:
                    if specific_deduction == 0 and specific_loan_amt == 0:
                        loan_amt = self.calculate_loan_amt(new_dict[values], values)
                    elif specific_deduction > 0 and specific_loan_amt == 0:
                        loan_amt = self.calculate_specific_deduction(specific_deduction, values)
                    elif specific_deduction == 0 and specific_loan_amt > 0:
                        loan_amt = self.specific_loan_amt

                    monthly_deduct = self.calculate_monthly_deduction(loan_amt, values)
                    admin_fee = self.calculate_admin_fee(loan_amt)
                    eligible_loan_amt = self.calculate_eligible_loan_amount(loan_amt, admin_fee)

                    lt_cont.append(values)
                    output_values.append(
                        f"Loan_amount: {round(eligible_loan_amt, -3) - 1000}  Loan_tenure: {values} months   Repayment: {monthly_deduct}   Admin Fee:{admin_fee}  Total balance: {round(loan_amt, -3)}"
                    )
                break

        for i in dict(map(lambda x, y: (x, y), lt_cont, output_values)).values():
            print(i)
            print('')

    def return_values(self):
        self.confirm_inputs()
        # self.interest_confirmation()
        self.netpay_loan_cal(self.specific_deduction, self.specific_loan_amt)


def run_loan_cal(prompt_one):
    counterx = 0
    while counterx < 1:
        valid_inputs = ['state1', 'state3', 'state5', 'state2', 'state4', 'state7', 'state8', 'state6']
        state_in = input(
            'select state - state1, state2, state3, state5, state4,state7, state8, state6 ')
        if state_in in valid_inputs:

            if prompt_one == 'N':
                netpay_in = input('Net salary: ')
                monthly_repayment_in = input('Existing repayment: Enter 0 if you there is no active loan  ')
                accrude_interest_in = input('Existing interest: Enter 0 if you there is no active loan  ')
                principal_balance_in = input('Existing loan balance: Enter 0 if you there is no active loan  ')
                specific_deduction_in, specific_loan_amt_in = ['0', '0']

            elif prompt_one == 'D':
                netpay_in, monthly_repayment_in, accrude_interest_in, principal_balance_in, specific_loan_amt_in = ['0',
                                                                                                                    '0',
                                                                                                                    '0',
                                                                                                                    '0',
                                                                                                                    '0']
                specific_deduction_in = input('Enter chosen repayment amount: ')

            elif prompt_one == 'L':
                netpay_in, monthly_repayment_in, accrude_interest_in, principal_balance_in, specific_deduction_in = ['0',
                                                                                                                     '0',
                                                                                                                     '0',
                                                                                                                     '0',
                                                                                                                     '0']
                specific_loan_amt_in = input('Enter loan amount: ')

            d2 = Loan_cal(state_in, netpay_in, monthly_repayment_in, accrude_interest_in, principal_balance_in,
                          specific_deduction_in, specific_loan_amt_in)
            d2.return_values()
        else:
            print("select a valid option from the list below")


def main_app():
    counter = 0
    while counter < 1:
        first_time_used = input("Do you have an account with JtestB. Select Yes or No  ")
        if first_time_used.lower() == "yes":
            First_name = input("Enter your first name  ")
            Last_name = input("Enter your last name  ")
            Email = input("What's your email  ")
            Mobile = input("Enter your mobile  ")
            City = input("Enter your city  ")
            print("Thank you for providing the requested info. We'll notify you as soon as we can proceed with your loan request. ")
            print("")

        elif first_time_used.lower() == "no":
            counter1 = 0
            while counter1 < 1:
                prompt_zero = input("Select loan category; A-salary loan  c-car loan ")
                if prompt_zero == "a":
                    counter2 = 0
                    while counter2 < 1:
                        prompt_one = input(
                            'Select loan type: N-Salary based,  L-Specific loan amount, D-I want a particular deduction ')
                        if prompt_one.lower() in ['n', 'd', 'l ']:
                            run_loan_cal(prompt_one)

                        else:
                            print('Invalid option selected. Select a valid option from the list below: ')
                            print("n   d   l")


                elif prompt_zero.lower() == "c":
                        print("")
                        print(
                            "Thank you for reaching out. We'll notify you as soon as our car loan services is fully available")
                        print("")
                        print("Do you wish to apply for a salary loan instead, simply select option A below to proceed")

                else:
                    print("select a valid option A OR B ")
        else:
            print("Invalid inputs entered")
            """use a function that will take user back to select a valid optionNo"""

main_app()