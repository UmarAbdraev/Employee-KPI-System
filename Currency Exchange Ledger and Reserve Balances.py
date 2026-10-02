# Списки резервов валют в кассе (index i):
curr_codes = [] # list[str]: Коды валют ("USD", "EUR", "GBP", "RUB")
curr_buy_rates = [] # list[float]: Курсы покупки валюты пунктом (в сомах)
curr_sell_rates = [] # list[float]: Курсы продажи валюты пунктом (в сомах)
curr_reserves = [] # list[float]: Наличные остатки каждой валюты в кассе

# Списки истории транзакций (index j): 
trans_client_ids = [] # list[str]: ИНН/Паспорт клиентов
trans_types = [] # list[str]: Тип операции ("BUY" или "SELL")
trans_currencies = [] # list[str]: Код обмениваемой валюты
trans_amounts = [] # list[float]: Объем операции в валюте
trans_rub_totals = [] # list[float]: Итоговая сумма операции в рублях

def init_currency(code, buy_rate, sell_rate, initial_reserve):
    if code not in curr_codes:
        curr_codes.append(code)
        curr_buy_rates.append(buy_rate)
        curr_sell_rates.append(sell_rate)
        curr_reserves.append(initial_reserve)
    else:
        return f'{code} already exists in {curr_codes}'

def calculate_cross_rate(from_curr, to_curr):
    from_idx = curr_codes.index(from_curr)
    to_idx = curr_codes.index(to_curr)
    Cross_Rate = curr_buy_rates[from_idx] / curr_sell_rates[to_idx]
    return Cross_Rate

def execute_transaction(client_id, trans_type, curr_code, amount):
    if curr_code in curr_codes:
        curr_idx = curr_codes.index(curr_code)
        rub_idx = curr_codes.index('RUB')
        if trans_type == 'BUY':
            if curr_reserves[curr_idx] >= amount:
                RUB_total = amount * curr_sell_rates[curr_idx]
                curr_reserves[curr_idx] -= amount
                curr_reserves[rub_idx] += RUB_total
                trans_client_ids.append(client_id)
                trans_types.append(trans_type)
                trans_currencies.append(curr_code)
                trans_amounts.append(amount)
                trans_rub_totals.append(RUB_total)
                print(f'{client_id} bought {amount} {curr_code} for {RUB_total} RUB.')
            else:
                print(f'Not enough {curr_code} in reserve to complete the transaction.')
        elif trans_type == 'SELL':
            if curr_reserves[rub_idx] >= amount * curr_buy_rates[curr_idx]:
                RUB_total = amount * curr_buy_rates[curr_idx]
                curr_reserves[curr_idx] += amount
                curr_reserves[rub_idx] -= RUB_total
                trans_client_ids.append(client_id)
                trans_types.append(trans_type)
                trans_currencies.append(curr_code)
                trans_amounts.append(amount)
                trans_rub_totals.append(RUB_total)
                print(f'{client_id} sold {amount} {curr_code} for {RUB_total} RUB.')
            else:
                print(f'Not enough RUB in reserve to complete the transaction.')
    else:
        print(f'{curr_code} does not exist in reserves.')

def client_transaction_history(client_id):
    for index, id in enumerate(trans_client_ids):
        if client_id == id:
            return f'Транзакции клиента {client_id}: Тип: {trans_types[index]}, Валюта: {trans_currencies[index]}, Сумма: {trans_amounts[index]}, Итог в RUB: {trans_rub_totals[index]}'

def aufit_vault_limits(min_rub_limit):
    if curr_reserves[curr_codes.index('RUB')] < min_rub_limit:
        print(f'LowCashReserveWarning: В кассе осталось {curr_reserves[curr_codes.index('RUB')]} RUB, что ниже лимита {min_rub_limit} RUB.')
    else:
        print(f'Все в порядке: В кассе осталось {curr_reserves[curr_codes.index('RUB')]} RUB. Лимит {min_rub_limit} RUB.')
