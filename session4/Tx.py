from io import BytesIO
import requests
from session4.helper import little_endian_to_int, read_varint, encode_varint, int_to_little_endian
from session4.Script import Script


class Tx:

    def __init__(self, version, tx_ins, tx_outs, locktime):
        self.version = version
        self.tx_ins = tx_ins
        self.tx_outs = tx_outs
        self.locktime = locktime

    def __repr__(self):
        tx_ins = ''
        for tx_in in self.tx_ins:
            tx_ins += tx_in.__repr__() + '\n'
        tx_outs = ''
        for tx_out in self.tx_outs:
            tx_outs += tx_out.__repr__() + '\n'
        return 'version: {}\ntx_ins:\n{}\ntx_outs:\n{}\nlocktime: {}\n'.format(
            self.version,
            tx_ins,
            tx_outs,
            self.locktime,
        )

    @classmethod
    def parse(cls, s):
        version = little_endian_to_int(s.read(4))
        num_inputs = read_varint(s)
        inputs = []

        for _ in range(num_inputs):
            inputs.append(TxIn.parse(s))

        num_outputs = read_varint(s)
        outputs = []

        for _ in range(num_outputs):
            outputs.append(TxOut.parse(s))

        locktime = little_endian_to_int(s.read(4))
        return cls(version, inputs, outputs, locktime)

    def serialize(self):
        result = int_to_little_endian(self.version, 4)
        result += encode_varint(len(self.tx_ins))
        for tx_in in self.tx_ins:
            result += tx_in.serialize()

        result += encode_varint(len(self.tx_outs))
        for tx_out in self.tx_outs:
            result += tx_out.serialize()

        result += int_to_little_endian(self.locktime, 4)
        return result

    def fee(self):
        input_sum, output_sum = 0, 0
        for tx_in in self.tx_ins:
            input_sum += tx_in.value()

        for tx_out in self.tx_outs:
            output_sum += tx_out.amount

        return input_sum - output_sum


class TxIn:

    cache = {}

    def __init__(self, prev_tx, prev_index, script_sig, sequence):
        self.prev_tx = prev_tx
        self.prev_index = prev_index
        self.script_sig = Script.parse(script_sig)
        self.sequence = sequence

    def __repr__(self):
        return '{}:{}'.format(
            self.prev_tx.hex(),
            self.prev_index,
        )

    @classmethod
    def parse(cls, s):
        prev_tx = s.read(32)[::-1]
        prev_index = little_endian_to_int(s.read(4))
        script_sig_length = read_varint(s)
        script_sig = s.read(script_sig_length)
        sequence = little_endian_to_int(s.read(4))
        return cls(prev_tx, prev_index, script_sig, sequence)

    def serialize(self):

        # reverse order
        result = self.prev_tx[::-1]
        result += int_to_little_endian(self.prev_index, 4)
        raw_script_sig = self.script_sig.serialize()
        result += encode_varint(len(raw_script_sig))
        result += raw_script_sig
        result += int_to_little_endian(self.sequence, 4)
        return result

    @classmethod
    def get_url(cls, testnet=False):
        if testnet:
            return 'https://testnet.blockexplorer.com/api'
        else:
            return 'https://blockexplorer.com/api'

    def fetch_tx(self, testnet=False):
        if self.prev_tx not in self.cache:
            url = self.get_url(testnet) + '/rawtx/{}'.format(self.prev_tx.hex())
            response = requests.get(url)
            try:
                js_response = response.json()
                if 'rawtx' not in js_response:
                    raise RuntimeError('got from server: {}'.format(js_response))
            except:
                raise RuntimeError('got from server: {}'.format(response.text))

            raw = bytes.fromhex(js_response['rawtx'])
            stream = BytesIO(raw)
            tx = Tx.parse(stream)
            self.cache[self.prev_tx] = tx
        return self.cache[self.prev_tx]

    def value(self, testnet=False):
        tx = self.fetch_tx(testnet=testnet)
        return tx.tx_outs[self.prev_index].amount


class TxOut:

    def __init__(self, amount, script_pubkey):
        self.amount = amount
        self.script_pubkey = Script.parse(script_pubkey)

    def __repr__(self):
        return '{}:{}'.format(self.amount, self.script_pubkey)

    @classmethod
    def parse(cls, s):
        amount = little_endian_to_int(s.read(8))
        script_pubkey_length = read_varint(s)
        script_pubkey = s.read(script_pubkey_length)
        return cls(amount, script_pubkey)

    def serialize(self):
        result = int_to_little_endian(self.amount)
        raw_script_pubkey = self.script_pubkey.serialize()
        result += encode_varint(len(raw_script_pubkey))
        result += raw_script_pubkey
        return result
