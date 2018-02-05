# Create your views here.
from uuid import uuid4

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from main.blockchain import BlockChain

blockchain = BlockChain()
node_identifier = str(uuid4()).replace('-', '')


class MineView(TemplateView):
    def get(self, request, *args, **kwargs):
        last_block = blockchain.last_block
        last_proof = last_block['proof']
        proof = blockchain.proof_of_work(last_proof)
        blockchain.new_transaction(
            sender="0",
            recipient=node_identifier,
            amount=1,
        )
        previous_hash = blockchain.hash(last_block)
        block = blockchain.new_block(proof, previous_hash)
        response = {
            'message': "New Block Forged",
            'index': block['index'],
            'transactions': block['transactions'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash'],
        }
        return JsonResponse(response, status=200)


class NewTransationView(TemplateView):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(NewTransationView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        values = request.POST
        required = ['sender', 'recipient', 'amount']
        if not all(k in values for k in required):
            return JsonResponse({'error': 'All values required'}, status=400)

        # Create a new Transaction
        index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

        response = {'message': f'Transaction will be added to Block {index}'}
        return JsonResponse(response, status=201)


class TrainView(TemplateView):
    def get(self, request, *args, **kwargs):
        response = {
            'chain': blockchain.chain,
            'length': len(blockchain.chain),
        }
        return JsonResponse(response, status=200)


class NodeResolveView(TemplateView):
    def get(self, request, *args, **kwargs):
        replaced = blockchain.resolve_conflicts()

        if replaced:
            response = {
                'message': 'Our chain was replaced',
                'new_chain': blockchain.chain
            }
        else:
            response = {
                'message': 'Our chain is authoritative',
                'chain': blockchain.chain
            }
        return JsonResponse(response, status=200)


class NodeRegisterView(TemplateView):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(NodeRegisterView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        values = request.POST
        nodes = values.get('nodes')
        if not nodes:
            return JsonResponse({'error': 'Error: Please supply a valid list of nodes'}, status=400)
        nodes = nodes.split(',')
        for node in nodes:
            blockchain.register_node(node)

        response = {
            'message': 'New nodes have been added',
            'total_nodes': list(blockchain.nodes),
        }
        return JsonResponse(response, status=201)
