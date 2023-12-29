from time import sleep
import requests

class auth():

    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = "https://api.mercadolibre.com"

    def request(self, method="GET", url="", headers=None, params=None):

        req_params = params if params != None else {}
        req_headers = headers if headers != None else {}

        while True:

            match method:
                case "GET":
                    response = requests.get(url=url, params=req_params, headers=req_headers)
                case "PUT":
                    response = requests.put(url=url, params=req_params, headers=req_headers)
                case "POST":
                    response = requests.post(url=url, params=req_params, headers=req_headers)
                case "DELETE":
                    response = requests.delete(url=url, params=req_params, headers=req_headers)
                case "HEAD":
                    response = requests.head(url=url, params=req_params, headers=req_headers)
                case "OPTIONS":
                    response = requests.options(url=url, params=req_params, headers=req_headers)

            if response.status_code == 200:
                return response
            elif response.status_code != 429:
                print(response.json())
                break
            else:
                sleep(5)

class anuncio(auth):

    def todos(self, seller_id):
        """
        Descrição da função
        """
        #Descrição da função

        asct = True #Acesso Só Com Token

        if asct and (self.access_token == "" or type(self.access_token) != str):
            print("Token inválido")
            return []

        url = self.base_url+f"/users/{seller_id}/items/search"

        params = {
            'access_token': self.access_token,
            'offset': 0
        }

        response = self.request("GET", url=url, params=params)

        if response:

            prods = []

            for prod in response.json()['results']:
                prods.append(prod)

            total = int(response.json()["paging"]["total"])
            limit = int(response.json()["paging"]["limit"])

            if total > limit:

                while total > len(prods):

                    params['offset'] += limit

                    response2 = requests.get(url, params=params)

                    for prod in response2.json()['results']:
                        prods.append(prod)

            return prods
        
        else:
            return []
        
    def unico(self, mlb):
        """
        Descrição da função
        """
        #Descrição da função

        asct = False #Acesso Só Com Token

        if asct and (self.access_token == "" or type(self.access_token) != str):
            print("Token inválido")
            return {}

        url = self.base_url+f"/items/{mlb}"

        params = {
            'access_token': self.access_token,
        }

        response = self.request("GET", url=url, params=params)

        if response:

            return response.json()
        
        else:
            return {}
        
    def taxa_venda(self, preco, id_tipo_listagem, id_categoria):
        """
        Descrição da função
        """
        #Descrição da função

        asct = False #Acesso Só Com Token

        if asct and (self.access_token == "" or type(self.access_token) != str):
            print("Token inválido")
            return {}

        url = self.base_url+f"/sites/MLB/listing_prices"

        params = {
            'access_token': self.access_token,
            'price': preco,
            'listing_type_id': id_tipo_listagem,
            'category_id': id_categoria
        }

        response = self.request("GET", url=url, params=params)

        if response:

            return response.json()
        
        else:
            return {}
        
    def opcoes_entrega(self, mlb, codigo_postal):
        """
        Descrição da função
        """
        #Descrição da função

        asct = False #Acesso Só Com Token

        if asct and (self.access_token == "" or type(self.access_token) != str):
            print("Token inválido")
            return {}

        url = self.base_url+f"/items/{mlb}/shipping_options"

        params = {
            'access_token': self.access_token,
            'zip_code': codigo_postal
        }

        response = self.request("GET", url=url, params=params)

        if response:

            return response.json()
        
        else:
            return {}
        
    def unico_extra(self, mlb):
        """
        Pega todas as informações do anúncio e também acrescenta a taxa de venda e o custo do frete grátis (caso seja).

        As informações estão dentro de 'body'
        Taxa de venda como 'sale_fee'
        Custo de frete grátis como 'shipping_free_cost'
        """
        #Descrição da função

        asct = False #Acesso Só Com Token

        if asct and (self.access_token == "" or type(self.access_token) != str):
            print("Token inválido")
            return {}

        url = self.base_url+f"/items/{mlb}"

        params = {
            'access_token': self.access_token,
        }

        response = self.request("GET", url=url, params=params)

        if response:

            anuncio = response.json()

            anuncio['sale_fee'] = self.taxa_venda(anuncio['price'], anuncio['listing_type_id'], anuncio['category_id'])['sale_fee_amount']
            if anuncio['shipping']['free_shipping'] == 1:
                anuncio['shipping_free_cost'] = self.opcoes_entrega(mlb, '04913000')['options'][0]['list_cost']
            else:
                anuncio['shipping_free_cost'] = 0

            return anuncio
        
        else:
            return {}
        
class vendedor(auth):

    def informacoes(self, seller_id):
        """
        Descrição da função
        """
        #Descrição da função

        asct = False #Acesso Só Com Token

        if asct and (self.access_token == "" or type(self.access_token) != str):
            print("Token inválido")
            return {}

        url = self.base_url+f"/users/{seller_id}"

        params = {
            'access_token': self.access_token,
        }

        response = self.request("GET", url=url, params=params)

        if response:

            return response.json()
        
        else:
            return {}
        