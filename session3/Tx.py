from io import BytesIO
from session3.helper import little_endian_to_int, read_varint, encode_varint


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


class TxIn:

    def __init__(self, prev_tx, prev_index, script_sig, sequence):
        self.prev_tx = prev_tx
        self.prev_index = prev_index
        self.scrip_sig = script_sig
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


class TxOut:

    def __init__(self, amount, script_pubkey):
        self.amount = amount
        self.script_pubkey = script_pubkey

    @classmethod
    def parse(cls, s):
        amount = little_endian_to_int(s.read(8))
        script_pubkey_length = read_varint(s)
        script_pubkey = s.read(script_pubkey_length)
        return cls(amount, script_pubkey)