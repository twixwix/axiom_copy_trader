import struct
from datetime import datetime
from solana.rpc.types import TokenAccountOpts, TxOpts
from spl.token.instructions import (
    CloseAccountParams,
    close_account,
    create_associated_token_account,
    get_associated_token_address,
)
from solders.compute_budget import set_compute_unit_limit, set_compute_unit_price  # type: ignore
from solders.instruction import Instruction, AccountMeta  # type: ignore
from solders.message import MessageV0  # type: ignore
from solders.transaction import VersionedTransaction  # type: ignore
from .config import client, payer_keypair, UNIT_BUDGET, UNIT_PRICE
from .constants import *
from .utils import confirm_txn, get_token_balance
from .coin_data import get_coin_data, sol_for_tokens, tokens_for_sol


def buy(mint_str: str, sol_in: float = 0.01, slippage: int = 5) -> bool:
    try:
        # print(f'Starting buy transaction for mint: {mint_str}')

        coin_data = get_coin_data(mint_str)
        
        if not coin_data:
            print(f'[{datetime.now()}] Failed [PF] to retrieve coin data while buying!')

            return False

        if coin_data.complete:
            print(f'[{datetime.now()}] Warning: This token [PF] has bonded and is only buyable on Raydium.')

            return

        MINT = coin_data.mint
        BONDING_CURVE = coin_data.bonding_curve
        ASSOCIATED_BONDING_CURVE = coin_data.associated_bonding_curve
        USER = payer_keypair.pubkey()

        # print('Fetching or creating associated token account...')
        try:
            ASSOCIATED_USER = client.get_token_accounts_by_owner(USER, TokenAccountOpts(MINT)).value[0].pubkey
            token_account_instruction = None
            # print(f'Token account found: {ASSOCIATED_USER}')
        except:
            ASSOCIATED_USER = get_associated_token_address(USER, MINT)
            token_account_instruction = create_associated_token_account(USER, USER, MINT)
            # print(f'Creating token account : {ASSOCIATED_USER}')

        # print('Calculating transaction amounts...')
        sol_dec = 1e9
        token_dec = 1e6
        virtual_sol_reserves = coin_data.virtual_sol_reserves / sol_dec
        virtual_token_reserves = coin_data.virtual_token_reserves / token_dec
        amount = sol_for_tokens(sol_in, virtual_sol_reserves, virtual_token_reserves)
        amount = int(amount * token_dec)
        
        slippage_adjustment = 1 + (slippage / 100)
        max_sol_cost = int((sol_in * slippage_adjustment) * sol_dec)
        # print(f'Amount: {amount}, Max Sol Cost: {max_sol_cost}')

        # print('Creating swap instructions...')
        keys = [
            AccountMeta(pubkey=GLOBAL, is_signer=False, is_writable=False),
            AccountMeta(pubkey=FEE_RECIPIENT, is_signer=False, is_writable=True),
            AccountMeta(pubkey=MINT, is_signer=False, is_writable=False),
            AccountMeta(pubkey=BONDING_CURVE, is_signer=False, is_writable=True),
            AccountMeta(pubkey=ASSOCIATED_BONDING_CURVE, is_signer=False, is_writable=True),
            AccountMeta(pubkey=ASSOCIATED_USER, is_signer=False, is_writable=True),
            AccountMeta(pubkey=USER, is_signer=True, is_writable=True),
            AccountMeta(pubkey=SYSTEM_PROGRAM, is_signer=False, is_writable=False),
            AccountMeta(pubkey=TOKEN_PROGRAM, is_signer=False, is_writable=False),
            AccountMeta(pubkey=RENT, is_signer=False, is_writable=False),
            AccountMeta(pubkey=EVENT_AUTHORITY, is_signer=False, is_writable=False),
            AccountMeta(pubkey=PUMP_FUN_PROGRAM, is_signer=False, is_writable=False)
        ]

        data = bytearray()
        data.extend(bytes.fromhex('66063d1201daebea'))
        data.extend(struct.pack('<Q', amount))
        data.extend(struct.pack('<Q', max_sol_cost))
        swap_instruction = Instruction(PUMP_FUN_PROGRAM, bytes(data), keys)

        instructions = [
            set_compute_unit_limit(UNIT_BUDGET),
            set_compute_unit_price(UNIT_PRICE),
        ]
        if token_account_instruction:
            instructions.append(token_account_instruction)
        instructions.append(swap_instruction)

        # print('Compiling transaction message...')
        compiled_message = MessageV0.try_compile(
            payer_keypair.pubkey(),
            instructions,
            [],
            client.get_latest_blockhash().value.blockhash,
        )

        # print('Sending transaction...')
        txn_sig = client.send_transaction(
            txn=VersionedTransaction(compiled_message, [payer_keypair]),
            opts=TxOpts(skip_preflight=True)
        ).value

        print(f'[{datetime.now()}] Buy [PF] transaction Signature: {txn_sig}')

        # print('Confirming transaction...')
        confirmed = confirm_txn(txn_sig)
        
        print(f'[{datetime.now()}] Buy [PF] transaction confirmed: {confirmed}')

        return confirmed
    except Exception as e:
        print(f'[{datetime.now()}] Error [PF] occurred during buy transaction: {e}')

        return False


def sell(mint_str: str, percentage: int = 100, slippage: int = 5) -> bool | None:
    try:
        # print(f'Starting sell transaction for mint: {mint_str}')

        if not (1 <= percentage <= 100):
            print(f'[{datetime.now()}] Percentage [PF] must be between 1 and 100.')

            return False

        coin_data = get_coin_data(mint_str)

        if not coin_data:
            print(f'[{datetime.now()}] Failed [PF] to retrieve coin data while selling.')

            return False

        if coin_data.complete:
            print(f'[{datetime.now()}] Warning: This token [PF] has bonded and is only sellable on Raydium.')

            return

        MINT = coin_data.mint
        BONDING_CURVE = coin_data.bonding_curve
        ASSOCIATED_BONDING_CURVE = coin_data.associated_bonding_curve
        USER = payer_keypair.pubkey()
        ASSOCIATED_USER = get_associated_token_address(USER, MINT)

        # print('Retrieving token balance...')
        token_balance = get_token_balance(payer_keypair.pubkey(), mint_str)

        if token_balance == 0 or token_balance is None:
            print(f'[{datetime.now()}] Token balance [PF] is zero. Nothing to sell.')

            return None

        print(f'[{datetime.now()}] Sell [PF] token Balance: {token_balance}')
        
        # print('Calculating transaction amounts...')
        sol_dec = 1e9
        token_dec = 1e6
        token_balance = token_balance * (percentage / 100)
        amount = int(token_balance * token_dec)
        
        virtual_sol_reserves = coin_data.virtual_sol_reserves / sol_dec
        virtual_token_reserves = coin_data.virtual_token_reserves / token_dec
        sol_out = tokens_for_sol(token_balance, virtual_sol_reserves, virtual_token_reserves)
        
        slippage_adjustment = 1 - (slippage / 100)
        min_sol_output = int((sol_out * slippage_adjustment) * sol_dec)
        # print(f'Amount: {amount}, Minimum Sol Out: {min_sol_output}')
        #
        # print('Creating swap instructions...')
        keys = [
            AccountMeta(pubkey=GLOBAL, is_signer=False, is_writable=False),
            AccountMeta(pubkey=FEE_RECIPIENT, is_signer=False, is_writable=True),
            AccountMeta(pubkey=MINT, is_signer=False, is_writable=False),
            AccountMeta(pubkey=BONDING_CURVE, is_signer=False, is_writable=True),
            AccountMeta(pubkey=ASSOCIATED_BONDING_CURVE, is_signer=False, is_writable=True),
            AccountMeta(pubkey=ASSOCIATED_USER, is_signer=False, is_writable=True),
            AccountMeta(pubkey=USER, is_signer=True, is_writable=True),
            AccountMeta(pubkey=SYSTEM_PROGRAM, is_signer=False, is_writable=False),
            AccountMeta(pubkey=ASSOC_TOKEN_ACC_PROG, is_signer=False, is_writable=False),
            AccountMeta(pubkey=TOKEN_PROGRAM, is_signer=False, is_writable=False),
            AccountMeta(pubkey=EVENT_AUTHORITY, is_signer=False, is_writable=False),
            AccountMeta(pubkey=PUMP_FUN_PROGRAM, is_signer=False, is_writable=False)
        ]

        data = bytearray()
        data.extend(bytes.fromhex('33e685a4017f83ad'))
        data.extend(struct.pack('<Q', amount))
        data.extend(struct.pack('<Q', min_sol_output))
        swap_instruction = Instruction(PUMP_FUN_PROGRAM, bytes(data), keys)

        instructions = [
            set_compute_unit_limit(UNIT_BUDGET),
            set_compute_unit_price(UNIT_PRICE),
            swap_instruction,
        ]

        if percentage == 100:
            # print('Preparing to close token account after swap...')
            close_account_instruction = close_account(CloseAccountParams(TOKEN_PROGRAM, ASSOCIATED_USER, USER, USER))
            instructions.append(close_account_instruction)

        # print('Compiling transaction message...')
        compiled_message = MessageV0.try_compile(
            payer_keypair.pubkey(),
            instructions,
            [],
            client.get_latest_blockhash().value.blockhash,
        )

        # print('Sending transaction...')
        txn_sig = client.send_transaction(
            txn=VersionedTransaction(compiled_message, [payer_keypair]),
            opts=TxOpts(skip_preflight=True)
        ).value

        print(f'[{datetime.now()}] Sell [PF] transaction Signature: {txn_sig}')

        # print('Confirming transaction...')
        confirmed = confirm_txn(txn_sig)
        
        print(f'[{datetime.now()}] Sell [PF] transaction confirmed: {confirmed}')

        return confirmed
    except Exception as e:
        print(f'[{datetime.now()}] Error [PF] occurred during sell transaction: {e}')

        return False
