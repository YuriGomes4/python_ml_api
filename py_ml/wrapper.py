from time import sleep
import requests

class auth():

    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = "https://api.mercadolibre.com"

    def request(self, method="GET", url="", headers=None, params=None, data=None):

        req_params = params if params != None else {}
        req_headers = headers if headers != None else {}
        req_data = data if data != None else {}

        while True:

            match method:
                case "GET":
                    response = requests.get(url=url, params=req_params, headers=req_headers, data=req_data)
                case "PUT":
                    response = requests.put(url=url, params=req_params, headers=req_headers, data=req_data)
                case "POST":
                    response = requests.post(url=url, params=req_params, headers=req_headers, data=req_data)
                case "DELETE":
                    response = requests.delete(url=url, params=req_params, headers=req_headers, data=req_data)
                case "HEAD":
                    response = requests.head(url=url, params=req_params, headers=req_headers, data=req_data)
                case "OPTIONS":
                    response = requests.options(url=url, params=req_params, headers=req_headers, data=req_data)

            if response.status_code == 200:
                return response
            elif response.status_code != 429:
                print(f"""Erro no retorno da API do Mercado Livre
Mensagem: {response.json()['message']}
URL: {url}
Metodo: {method}
Parametros: {req_params}
Headers: {req_headers}
Data: {req_data}
JSON: {response.json()}""")
                break
            else:
                sleep(5)

    def refresh_token(self, client_id, client_secret, refresh_token):
        """
        Descrição da função
        """
        #Descrição da função

        asct = True #Acesso Só Com Token

        if asct and (self.access_token == "" or type(self.access_token) != str):
            print("Token inválido")
            return None
        
        seller_id = self.access_token.split('-')[-1]
        print(seller_id)

        url = self.base_url+f"/users/{seller_id}/items/search"

        params = {
            'access_token': self.access_token,
        }

        response = self.request("GET", url=url, params=params)

        if response:
            return None
        else:

            headers = {
                'accept': 'application/json',
                'content-type': 'application/x-www-form-urlencoded',
            }

            data = {
                'grant_type': 'refresh_token',
                'client_id': client_id,
                'client_secret': client_secret,
                'refresh_token': refresh_token,
            }

            #response = requests.post(f'{self.base_url}/oauth/token', headers=headers, data=data)

            response = self.request("POST", url=f'{self.base_url}/oauth/token', headers=headers, data=data)

            if response:
                return response
            else:
                return None

class anuncio:

    class get(auth):

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

        def descricao(self, mlb):
            """
            Descrição da função
            """
            #Descrição da função

            asct = True #Acesso Só Com Token

            if asct and (self.access_token == "" or type(self.access_token) != str):
                print("Token inválido")
                return {}

            url = self.base_url+f"/items/{mlb}/description"

            params = {
                'access_token': self.access_token,
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
                    opcoes = self.opcoes_entrega(mlb, '04913000')
                    if opcoes != {}:
                        anuncio['shipping_free_cost'] = opcoes['options'][0]['list_cost']
                    else:
                        anuncio['shipping_free_cost'] = 0
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
        
    def refresh_token(self, client_id, client_secret, refresh_token):
        return super().refresh_token(client_id, client_secret, refresh_token)
        
class venda(auth):

    def todas(self, seller_id):
        """
        Descrição da função
        """
        #Descrição da função

        asct = True #Acesso Só Com Token

        if asct and (self.access_token == "" or type(self.access_token) != str):
            print("Token inválido")
            return []

        url = self.base_url+f"/orders/search"

        params = {
            'access_token': self.access_token,
            'seller': seller_id,
            'q': "",
            'offset': 0
        }

        response = self.request("GET", url=url, params=params)

        if response:

            items = []

            for item in response.json()['results']:
                items.append(item)

            total = int(response.json()["paging"]["total"])
            limit = int(response.json()["paging"]["limit"])

            if total > limit:

                while total > len(items):

                    params['offset'] += limit

                    response2 = requests.get(url, params=params)

                    for item in response2.json()['results']:
                        items.append(item)

            return items
        
        else:
            return []

    def unica(self, id_venda):
        """
        Descrição da função
        """
        #Descrição da função

        asct = True #Acesso Só Com Token

        if asct and (self.access_token == "" or type(self.access_token) != str):
            print("Token inválido")
            return {}

        url = self.base_url+f"/orders/{id_venda}"

        params = {
            'access_token': self.access_token,
        }

        response = self.request("GET", url=url, params=params)

        if response:

            return response.json()
        
        else:
            return {}

    def info_envio(self, id_venda):
        """
        Descrição da função
        """
        #Descrição da função

        asct = True #Acesso Só Com Token

        if asct and (self.access_token == "" or type(self.access_token) != str):
            print("Token inválido")
            return {}

        url = self.base_url+f"/orders/{id_venda}/shipments"

        params = {
            'access_token': self.access_token,
        }

        response = self.request("GET", url=url, params=params)

        if response:

            return response.json()
        
        else:
            return {}  

    def info_faturamento(self, id_venda):
        """
        Descrição da função
        """
        #Descrição da função

        asct = True #Acesso Só Com Token

        if asct and (self.access_token == "" or type(self.access_token) != str):
            print("Token inválido")
            return {}

        url = self.base_url+f"/orders/{id_venda}/billing_info"

        params = {
            'access_token': self.access_token,
        }

        response = self.request("GET", url=url, params=params)

        if response:

            return response.json()
        
        else:
            return {}
        
    def unica_extra(self, id_venda):
        """
        Pega todas as informações da venda e também acrescenta informações do envio.

        As informações de envio estão dentro de 'shipping'
        """
        #Descrição da função

        asct = True #Acesso Só Com Token

        if asct and (self.access_token == "" or type(self.access_token) != str):
            print("Token inválido")
            return {}

        item = self.unica(id_venda)

        if item != {}:

            info_envio = self.info_envio(id_venda)

            if info_envio != {}:
                item['shipping'] = info_envio

            return item
        
        else:
            return {}