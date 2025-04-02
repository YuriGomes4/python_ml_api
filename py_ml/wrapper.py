import json
from time import sleep
import requests

class auth():

    def __init__(self, access_token="", print_error=True):
        self.access_token = access_token
        self.base_url = "https://api.mercadolibre.com"
        self.print_error = print_error

    def request(self, method="GET", url="", headers=None, params=None, data=None):

        req_params = params if params != None else {}
        req_headers = headers if headers != None else {}
        req_data = data if data != None else {}

        if self.access_token != "" and self.access_token != None:
            req_params['access_token'] = self.access_token

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

            if response.status_code == 200 or response.status_code == 201:
                return response
            elif response.status_code != 429:
                if self.print_error:
                    print(f"""Erro no retorno da API do Mercado Livre
Mensagem: {response.json()['message'] if 'message' in response.json() else ""}
URL: {url}
Metodo: {method}
Parametros: {req_params}
Headers: {req_headers}
Data: {req_data}
Resposta JSON: {response.json()}""")
                break
            else:
                sleep(5)

    def refresh_token(self, client_id, client_secret, refresh_token):
        """
        Descrição da função
        """
        #Descrição da função

        asct = True #Acesso Só Com Token

        if asct and (self.access_token == "" or self.access_token == None or type(self.access_token) != str):
            print("Token inválido")
            return None
        
        seller_id = self.access_token.split('-')[-1]

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

class geral:

    class get(auth):

        def categorias(self):
            """
            Descrição da função
            """
            #Descrição da função

            asct = False #Acesso Só Com Token

            if asct and (self.access_token == "" or self.access_token == None or type(self.access_token) != str):
                print("Token inválido")
                return {}

            url = self.base_url+f"/sites/MLB/categories"

            response = self.request("GET", url=url)

            if response:

                return response.json()
            
            else:
                return {}
            
        def preditor_categorias(self, q, limit=3):
            """
            Descrição da função
            """
            #Descrição da função

            asct = False #Acesso Só Com Token

            if asct and (self.access_token == "" or self.access_token == None or type(self.access_token) != str):
                print("Token inválido")
                return {}

            url = self.base_url+f"/sites/MLB/domain_discovery/search"

            params = {}

            if self.access_token != "":
                params['access_token'] = self.access_token

            if q != "":
                params['q'] = q
            else:
                print("Necessário informar uma pesquisa")
                return {}

            response = self.request("GET", url=url, params=params)

            if response:

                return response.json()
            
            else:
                return {}
            
        def detalhes_categoria(self, id_categoria):
            """
            Descrição da função
            """
            #Descrição da função

            asct = False #Acesso Só Com Token

            if asct and (self.access_token == "" or self.access_token == None or type(self.access_token) != str):
                print("Token inválido")
                return {}

            url = self.base_url+f"/categories/{id_categoria}"

            response = self.request("GET", url=url)

            if response:

                return response.json()
            
            else:
                return {}
            
        def mais_vendidos(self, id_categoria):
            """
            Descrição da função
            """
            #Descrição da função

            asct = True #Acesso Só Com Token

            if asct and (self.access_token == "" or self.access_token == None or type(self.access_token) != str):
                print("Token inválido")
                return {}
            
            params = {
                'access_token': self.access_token
            }

            url = self.base_url+f"/highlights/MLB/category/{id_categoria}"

            response = self.request("GET", url=url, params=params)

            if response:

                return response.json()
            
            else:
                return {}

class anuncio:

    class get(auth):

        def todos(self, seller_id):
            """
            Ver todos os anúncios do vendedor
            """
            #Descrição da função

            asct = True #Acesso Só Com Token

            if asct and (self.access_token == "" or self.access_token == None or type(self.access_token) != str):
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

            if asct and (self.access_token == "" or self.access_token == None or type(self.access_token) != str):
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
        
        def varios(self, mlbs):
            """
            Descrição da função
            """
            #Descrição da função

            asct = True #Acesso Só Com Token

            if asct and (self.access_token == "" or self.access_token == None or type(self.access_token) != str):
                print("Token inválido")
                return {}

            url = self.base_url+f"/items"

            params = {
                'access_token': self.access_token,
                'ids': ','.join(mlbs),
            }

            response = self.request("GET", url=url, params=params)

            if response:

                return response.json()
            
            else:
                return []

        def pesquisar(self, pesquisa, offset=0, **kwargs):
            """
            Descrição da função
            """
            #Descrição da função

            asct = False #Acesso Só Com Token

            if asct and (self.access_token == "" or self.access_token == None or type(self.access_token) != str):
                print("Token inválido")
                return {}

            url = self.base_url+f"/products/search"

            params = {
                'q': pesquisa,
                'offset': offset,
                'site_id': 'MLB',
                'status': 'active',
            }

            arg_dict = {}

            if 'arg_dict' in kwargs:
                arg_dict = kwargs['arg_dict']

            if kwargs != {}:
                for key, value in kwargs.items():
                    if key != 'arg_dict':
                        if key in arg_dict:
                            params[arg_dict[key]] = value
                        else:
                            params[key] = value

            response = self.request("GET", url=url, params=params)

            if response:

                return response.json()
            
            else:
                return {}
            
        def taxa_venda(self, preco, id_tipo_listagem, id_categoria, **kwargs):
            """
            Descrição da função
            """
            #Descrição da função

            asct = False #Acesso Só Com Token

            if asct and (self.access_token == "" or self.access_token == None or type(self.access_token) != str):
                print("Token inválido")
                return {}

            url = self.base_url+f"/sites/MLB/listing_prices"

            params = {
                'access_token': self.access_token,
                'price': preco,
                'listing_type_id': id_tipo_listagem,
                'category_id': id_categoria
            }

            arg_dict = {}

            if 'arg_dict' in kwargs:
                arg_dict = kwargs['arg_dict']

            if kwargs != {}:
                for key, value in kwargs.items():
                    if key != 'arg_dict':
                        if key in arg_dict:
                            params[arg_dict[key]] = value
                        else:
                            params[key] = value

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

            if asct and (self.access_token == "" or self.access_token == None or type(self.access_token) != str):
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

            asct = False #Acesso Só Com Token

            if asct and (self.access_token == "" or self.access_token == None or type(self.access_token) != str):
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

        def unico_extra(self, mlb, **kwargs):
            """
            Pega todas as informações do anúncio e também acrescenta a taxa de venda e o custo do frete grátis (caso seja).
            EXCLUSIVO PARA ANÚNCIOS DO VENDEDOR

            As informações estão dentro de 'body'
            Taxa de venda como 'sale_fee'
            Custo de frete grátis como 'shipping_free_cost'
            """
            #Descrição da função

            asct = True #Acesso Só Com Token

            if asct and (self.access_token == "" or self.access_token == None or type(self.access_token) != str):
                print("Token inválido")
                return {}

            url = self.base_url+f"/items/{mlb}"

            params = {
                'access_token': self.access_token,
            }

            arg_dict = {}

            if 'arg_dict' in kwargs:
                arg_dict = kwargs['arg_dict']

            if kwargs != {}:
                for key, value in kwargs.items():
                    if key != 'arg_dict':
                        if key in arg_dict:
                            params[arg_dict[key]] = value
                        else:
                            params[key] = value

            response = self.request("GET", url=url, params=params)

            if response:

                anuncio = response.json()

                if "supermarket_eligible" in anuncio['tags'] and anuncio['shipping']['logistic_type'] == "fulfillment":
                    resp_taxa_venda = self.taxa_venda(anuncio['price'], anuncio['listing_type_id'], anuncio['category_id'], tags="supermarket_eligible")
                else:
                    resp_taxa_venda = self.taxa_venda(anuncio['price'], anuncio['listing_type_id'], anuncio['category_id'])

                anuncio['sale_fee'] = resp_taxa_venda['sale_fee_amount']
                anuncio['sale_fee_tax'] = round(float(resp_taxa_venda['sale_fee_amount']) - float(resp_taxa_venda['sale_fee_details']['fixed_fee']), 2)
                anuncio['sale_fee_percentage'] = resp_taxa_venda['sale_fee_details']['percentage_fee']
                anuncio['sale_fee_fixed'] = resp_taxa_venda['sale_fee_details']['fixed_fee']
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
            
        def buscar_item_extra(self, mlb, **kwargs):
            """
            Pega todas as informações do anúncio e também acrescenta a taxa de venda e o custo do frete grátis (caso seja).

            As informações estão dentro de 'body'
            Taxa de venda como 'sale_fee'
            Custo de frete grátis como 'shipping_free_cost'
            """
            #Descrição da função

            asct = True #Acesso Só Com Token

            if asct and (self.access_token == "" or self.access_token == None or type(self.access_token) != str):
                print("Token inválido")
                return {}

            url = self.base_url+f"/items"

            if ',' in mlb:
                print("Apenas um mlb por vez")
                return {}

            params = {
                'access_token': self.access_token,
                'ids': mlb,
            }

            arg_dict = {}

            if 'arg_dict' in kwargs:
                arg_dict = kwargs['arg_dict']

            if kwargs != {}:
                for key, value in kwargs.items():
                    if key != 'arg_dict':
                        if key in arg_dict:
                            params[arg_dict[key]] = value
                        else:
                            params[key] = value

            response = self.request("GET", url=url, params=params)

            if response:

                anuncio = response.json()[0]['body']

                if "supermarket_eligible" in anuncio['tags'] and anuncio['shipping']['logistic_type'] == "fulfillment":
                    resp_taxa_venda = self.taxa_venda(anuncio['price'], anuncio['listing_type_id'], anuncio['category_id'], tags="supermarket_eligible")
                else:
                    resp_taxa_venda = self.taxa_venda(anuncio['price'], anuncio['listing_type_id'], anuncio['category_id'])

                anuncio['sale_fee'] = resp_taxa_venda['sale_fee_amount']
                anuncio['sale_fee_tax'] = round(float(resp_taxa_venda['sale_fee_amount']) - float(resp_taxa_venda['sale_fee_details']['fixed_fee']), 2)
                anuncio['sale_fee_percentage'] = resp_taxa_venda['sale_fee_details']['percentage_fee']
                anuncio['sale_fee_fixed'] = resp_taxa_venda['sale_fee_details']['fixed_fee']
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
            
        def promocoes(self, mlb):
            """
            Descrição da função
            """
            #Descrição da função

            asct = True #Acesso Só Com Token

            if asct and (self.access_token == "" or self.access_token == None or type(self.access_token) != str):
                print("Token inválido")
                return []

            url = self.base_url+f"/seller-promotions/items/{mlb}"

            params = {
                'app_version': 'v2',
                'access_token': self.access_token,
            }

            response = self.request("GET", url=url, params=params)

            if response:

                return response.json()
            
            else:
                return []
            
        def visitas_intervalo(self, mlb, dias, intervalo, termino):
            """
            Descrição da função

            Exemplo:
            last: 30
            unit: day
            ending: 2023-12-15
            """
            #Descrição da função

            asct = False #Acesso Só Com Token

            if asct and (self.access_token == "" or self.access_token == None or type(self.access_token) != str):
                print("Token inválido")
                return []

            url = self.base_url+f"/items/{mlb}/visits/time_window"

            params = {
                'last': dias,
                'unit': intervalo,
                'ending': termino,
            }

            if not(self.access_token == "" or self.access_token == None or type(self.access_token) != str):
                params['access_token'] = self.access_token

            response = self.request("GET", url=url, params=params)

            if response:

                return response.json()
            
            else:
                return []
            
        def visitas(self, mlb, **kwargs):
            """
            Ver o total de visitas de um anúncio
            """
            #Descrição da função

            asct = False #Acesso Só Com Token

            if asct and (self.access_token == "" or self.access_token == None or type(self.access_token) != str):
                print("Token inválido")
                return []

            url = self.base_url+f"/visits/items"

            params = {
                'ids': mlb,
            }

            arg_dict = {}

            if 'arg_dict' in kwargs:
                arg_dict = kwargs['arg_dict']

            if kwargs != {}:
                for key, value in kwargs.items():
                    if key != 'arg_dict':
                        if key in arg_dict:
                            params[arg_dict[key]] = value
                        else:
                            params[key] = value

            if not(self.access_token == "" or self.access_token == None or type(self.access_token) != str):
                params['access_token'] = self.access_token

            response = self.request("GET", url=url, params=params)

            if response:

                return response.json()
            
            else:
                return {}
            
        def catalogo(self, id_catalogo):
            """
            Descrição da função
            """
            #Descrição da função

            asct = False #Acesso Só Com Token

            if asct and (self.access_token == "" or self.access_token == None or type(self.access_token) != str):
                print("Token inválido")
                return {}

            url = self.base_url+f"/products/{id_catalogo}"

            params = {
                'access_token': self.access_token,
            }

            response = self.request("GET", url=url, params=params)

            if response:

                return response.json()
            
            else:
                return {}
        
        def custo_envio_gratis(self, seller_id, item_id=None, dimensions=None, **kwargs):
            """
            Descrição da função
            """
            #Descrição da função

            asct = True #Acesso Só Com Token

            if asct and (self.access_token == "" or self.access_token == None or type(self.access_token) != str):
                print("Token inválido")
                return {}
            
            url = self.base_url+f"/users/{seller_id}/shipping_options/free"
            
            params = {
                'access_token': self.access_token,
                'verbose': 'true',
            }

            if item_id != None:
                params['item_id'] = item_id
            elif dimensions != None:
                params['dimensions'] = dimensions
            else:
                print("Necessário informar item_id ou dimensions")
                return {}
            
            arg_dict = {}

            if 'arg_dict' in kwargs:
                arg_dict = kwargs['arg_dict']

            if kwargs != {}:
                for key, value in kwargs.items():
                    if key != 'arg_dict':
                        if key in arg_dict:
                            params[arg_dict[key]] = value
                        else:
                            params[key] = value

            response = self.request("GET", url=url, params=params)

            if response:
                    
                    return response.json()
            
            else:
                return {}

        def metricas_ads(self, item_id, **kwargs):
            """
            Descrição da função
            """
            #Descrição da função

            asct = True

            if asct and (self.access_token == "" or self.access_token == None or type(self.access_token) != str):
                print("Token inválido")
                return {}
            
            url = self.base_url+f"/advertising/product_ads/items/{item_id}"

            params = {
                'access_token': self.access_token,
            }

            arg_dict = {}

            if 'arg_dict' in kwargs:
                arg_dict = kwargs['arg_dict']

            if kwargs != {}:
                for key, value in kwargs.items():
                    if key != 'arg_dict':
                        if key in arg_dict:
                            params[arg_dict[key]] = value
                        else:
                            params[key] = value

            headers = {
                'api-version': '2'
            }

            response = self.request("GET", url=url, params=params, headers=headers)

            if response:
                    
                    return response.json()
            
            else:
                return {}

    class post(auth):

        def publicar_unico(self, dados={}, **kwargs):
            """
            Descrição da função
            """
            #Descrição da função

            asct = False #Acesso Só Com Token

            if asct and (self.access_token == "" or self.access_token == None or type(self.access_token) != str):
                print("Token inválido")
                return {}

            url = self.base_url+f"/items"

            params = {
                'access_token': self.access_token,
            }

            arg_dict = {}

            if 'arg_dict' in kwargs:
                arg_dict = kwargs['arg_dict']

            if kwargs != {}:
                for key, value in kwargs.items():
                    if key != 'arg_dict':
                        if key in arg_dict:
                            params[arg_dict[key]] = value
                        else:
                            params[key] = value

            headers = {
                'Content-Type': 'application/json'
            }

            response = self.request("POST", url=url, params=params, headers=headers, data=json.dumps(dados))

            if response:

                return response.json()
            
            else:
                return {}

class vendedor(auth):

    def informacoes(self, seller_id):
        """
        Descrição da função
        """
        #Descrição da função

        asct = False #Acesso Só Com Token

        if asct and (self.access_token == "" or self.access_token == None or type(self.access_token) != str):
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
    
    def loja_oficial(self, seller_id, official_store_id):
        """
        Descrição da função
        """
        #Descrição da função

        asct = False

        if asct and (self.access_token == "" or self.access_token == None or type(self.access_token) != str):
            print("Token inválido")
            return {}

        url = self.base_url+f"/users/{seller_id}/brands/{official_store_id}"

        params = {
            'access_token': self.access_token,
        }

        response = self.request("GET", url=url, params=params)

        if response:

            return response.json()
        
        else:
            return {}
        
class venda(auth):

    def todas(self, seller_id, **kwargs):
        """
        Descrição da função
        """
        #Descrição da função

        asct = True #Acesso Só Com Token

        if asct and (self.access_token == "" or self.access_token == None or type(self.access_token) != str):
            print("Token inválido")
            return []

        url = self.base_url+f"/orders/search"

        params = {
            'access_token': self.access_token,
            'seller': seller_id,
            'offset': 0
        }

        arg_dict = {}

        if 'arg_dict' in kwargs:
            arg_dict = kwargs['arg_dict']

        if kwargs != {}:
            for key, value in kwargs.items():
                if key != 'arg_dict':
                    if key in arg_dict:
                        params[arg_dict[key]] = value
                    else:
                        params[key] = value
        else:
            params['q'] = ''

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

        if asct and (self.access_token == "" or self.access_token == None or type(self.access_token) != str):
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

        if asct and (self.access_token == "" or self.access_token == None or type(self.access_token) != str):
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

        if asct and (self.access_token == "" or self.access_token == None or type(self.access_token) != str):
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

        if asct and (self.access_token == "" or self.access_token == None or type(self.access_token) != str):
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
