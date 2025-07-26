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
            req_headers['Authorization'] = f'Bearer {self.access_token}'

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
                    try:
                        response_json = response.json()
                        message = response_json['message'] if 'message' in response_json else ""
                        json_content = response_json
                    except:
                        message = ""
                        json_content = response.text
                    
                    print(f"""Erro no retorno da API do Mercado Livre
Mensagem: {message}
URL: {url}
Metodo: {method}
Parametros: {req_params}
Headers: {req_headers}
Data: {req_data}
Resposta JSON: {json_content}""")
                if response.status_code == 403 or response.status_code == 404:
                    return None
                else:
                    break
            else:
                sleep(5)

    def refresh_token(self, client_id, client_secret, refresh_token):
        """
        Descrição da função
        """
        #Descrição da função

        asct = False #Acesso Só Com Token

        if asct and (self.access_token == "" or self.access_token == None or type(self.access_token) != str):
            print("Token inválido")
            return None
        
        seller_id = refresh_token.split('-')[-1]

        url = self.base_url+f"/users/{seller_id}/items/search"

        response = self.request("GET", url=url)

        if response:
            return None
        else:

            self.access_token = None

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

            url = self.base_url+f"/highlights/MLB/category/{id_categoria}"

            response = self.request("GET", url=url)

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
                'offset': 0
            }

            response = self.request("GET", url=url, params=params)

            if response:

                total = int(response.json()["paging"]["total"])
                limit = int(response.json()["paging"]["limit"])

                prods = []

                if total > 1000:

                    params['search_type'] = 'scan'

                    response2 = self.request("GET", url=url, params=params)

                    if response2:
                        params['scroll_id'] = response2.json()['scroll_id']
                        params['offset'] = -100
                        limit = 100
                        params['limit'] = limit

                else:

                    for prod in response.json()['results']:
                        prods.append(prod)

                if total > limit:

                    while total > len(prods):

                        params['offset'] += limit

                        if ('scroll_id' not in params and params['offset'] > 1000) or params['offset'] > 10000:
                            break

                        if params['offset'] == 10000:
                            params['offset'] = 9999

                        response2 = self.request("GET", url=url, params=params)

                        if response2:

                            for prod in response2.json()['results']:
                                prods.append(prod)

                            if 'scroll_id' in params:
                                params['scroll_id'] = response2.json()['scroll_id']

                if total > 10000:

                    params['offset'] = limit*-1
                    params['status'] = 'active'

                    while total > len(prods):

                        params['offset'] += limit

                        if ('scroll_id' not in params and params['offset'] > 1000) or params['offset'] > 10000:
                            break

                        if params['offset'] == 10000:
                            params['offset'] = 9999

                        response2 = self.request("GET", url=url, params=params)

                        if response2:

                            for prod in response2.json()['results']:
                                prods.append(prod)

                            if 'scroll_id' in params:
                                params['scroll_id'] = response2.json()['scroll_id']

                        if len(response2.json()['results']) == 0:
                            break

                    params['offset'] = limit*-1
                    params['status'] = 'paused'

                    while total > len(prods):

                        params['offset'] += limit

                        if ('scroll_id' not in params and params['offset'] > 1000) or params['offset'] > 10000:
                            break

                        if params['offset'] == 10000:
                            params['offset'] = 9999

                        response2 = self.request("GET", url=url, params=params)

                        if response2:

                            for prod in response2.json()['results']:
                                prods.append(prod)

                            if 'scroll_id' in params:
                                params['scroll_id'] = response2.json()['scroll_id']

                        if len(response2.json()['results']) == 0:
                            break

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

            response = self.request("GET", url=url)

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
                'ids': ','.join(mlbs),
            }

            response = self.request("GET", url=url, params=params)

            if response:

                return response.json()
            
            else:
                return []

        def varios_extra(self, mlbs, **kwargs):
            """
            Pega todas as informações de vários anúncios e também acrescenta a taxa de venda e o custo do frete grátis (caso seja).
            EXCLUSIVO PARA ANÚNCIOS DO VENDEDOR

            As informações estão dentro de cada item
            Taxa de venda como 'sale_fee'
            Custo de frete grátis como 'shipping_free_cost'
            ID do preço como 'price_id'
            """
            #Descrição da função

            asct = True #Acesso Só Com Token

            if asct and (self.access_token == "" or self.access_token == None or type(self.access_token) != str):
                print("Token inválido")
                return []

            url = self.base_url+f"/items"

            params = {
                'ids': ','.join(mlbs),
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

                anuncios_processados = []
                
                for item in response.json():
                    if item['code'] == 200:
                        anuncio = item['body']

                        if "supermarket_eligible" in anuncio['tags'] and anuncio['shipping']['logistic_type'] == "fulfillment":
                            resp_taxa_venda = self.taxa_venda(anuncio['price'], anuncio['listing_type_id'], anuncio['category_id'], tags="supermarket_eligible")
                        else:
                            resp_taxa_venda = self.taxa_venda(anuncio['price'], anuncio['listing_type_id'], anuncio['category_id'])

                        anuncio['sale_fee'] = resp_taxa_venda['sale_fee_amount']
                        anuncio['sale_fee_tax'] = round(float(resp_taxa_venda['sale_fee_amount']) - float(resp_taxa_venda['sale_fee_details']['fixed_fee']), 2)
                        anuncio['sale_fee_percentage'] = resp_taxa_venda['sale_fee_details']['percentage_fee']
                        anuncio['sale_fee_fixed'] = resp_taxa_venda['sale_fee_details']['fixed_fee']
                        
                        if anuncio['shipping']['free_shipping'] == 1:
                            custo_frete_gratis = self.custo_envio_gratis(anuncio['seller_id'], item_id=anuncio['id'])
                            if "coverage" in custo_frete_gratis:
                                if "all_country" in custo_frete_gratis['coverage']:
                                    if "list_cost" in custo_frete_gratis['coverage']['all_country']:
                                        anuncio['shipping_free_cost'] = custo_frete_gratis['coverage']['all_country']['list_cost']
                                    else:
                                        anuncio['shipping_free_cost'] = 0
                                else:
                                    anuncio['shipping_free_cost'] = 0
                            else:
                                anuncio['shipping_free_cost'] = 0
                        else:
                            anuncio['shipping_free_cost'] = 0

                        resposta_preco = self.precos(anuncio['id'])
                        if resposta_preco != {}:
                            anuncio['price_id'] = resposta_preco['price_id']
                            anuncio['price'] = resposta_preco['amount']
                            anuncio['base_price'] = resposta_preco['regular_amount']
                        else:
                            anuncio['price_id'] = None

                        anuncios_processados.append(anuncio)
                    else:
                        # Mantém a estrutura original para itens que falharam
                        anuncios_processados.append(item)

                return anuncios_processados
            
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

            asct = True #Acesso Só Com Token

            if asct and (self.access_token == "" or self.access_token == None or type(self.access_token) != str):
                print("Token inválido")
                return {}

            url = self.base_url+f"/sites/MLB/listing_prices"

            params = {
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

            response = self.request("GET", url=url)

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
            ID do preço como 'price_id'
            """
            #Descrição da função

            asct = True #Acesso Só Com Token

            if asct and (self.access_token == "" or self.access_token == None or type(self.access_token) != str):
                print("Token inválido")
                return {}

            url = self.base_url+f"/items/{mlb}"

            params = {}

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
                    custo_frete_gratis = self.custo_envio_gratis(anuncio['seller_id'], item_id=anuncio['id'])
                    if "coverage" in custo_frete_gratis:
                        if "all_country" in custo_frete_gratis['coverage']:
                            if "list_cost" in custo_frete_gratis['coverage']['all_country']:
                                anuncio['shipping_free_cost'] = custo_frete_gratis['coverage']['all_country']['list_cost']
                            else:
                                anuncio['shipping_free_cost'] = 0
                        else:
                            anuncio['shipping_free_cost'] = 0
                    else:
                        anuncio['shipping_free_cost'] = 0
                else:
                    anuncio['shipping_free_cost'] = 0

                resposta_preco = self.precos(mlb)
                if resposta_preco != {}:
                    anuncio['price_id'] = resposta_preco['price_id']
                    anuncio['price'] = resposta_preco['amount']
                    anuncio['base_price'] = resposta_preco['regular_amount']
                else:
                    anuncio['price_id'] = None

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
                    custo_frete_gratis = self.custo_envio_gratis(anuncio['seller_id'], item_id=anuncio['id'])
                    if "coverage" in custo_frete_gratis:
                        if "all_country" in custo_frete_gratis['coverage']:
                            if "list_cost" in custo_frete_gratis['coverage']['all_country']:
                                anuncio['shipping_free_cost'] = custo_frete_gratis['coverage']['all_country']['list_cost']
                            else:
                                anuncio['shipping_free_cost'] = 0
                        else:
                            anuncio['shipping_free_cost'] = 0
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
            }

            response = self.request("GET", url=url, params=params)

            if response:

                return response.json()
            
            else:
                return []
            
        def visitas_intervalo(self, item_id, last, unit, ending=None):
            """
            Visitantes por data por anúncio em janela de tempo
            
            Args:
                item_id: ID do anúncio
                last: Quantos períodos antes (ex: 30)
                unit: Unidade de tempo ("day")
                ending: Data de fim opcional (formato ISO: YYYY-MM-DD)
            
            Exemplo:
                last: 30
                unit: "day"
                ending: "2023-12-15"
            """
            #Descrição da função

            asct = False #Acesso Só Com Token

            if asct and (self.access_token == "" or self.access_token == None or type(self.access_token) != str):
                print("Token inválido")
                return {}

            url = self.base_url+f"/items/{item_id}/visits/time_window"

            params = {
                'last': last,
                'unit': unit,
            }

            if ending:
                params['ending'] = ending

            response = self.request("GET", url=url, params=params)

            if response:
                return response.json()
            else:
                return {}
            
        def visitas(self, item_ids, **kwargs):
            """
            Ver o total de visitas de um ou vários anúncios
            
            Args:
                item_ids: ID(s) do(s) anúncio(s) - pode ser string única ou lista
            """
            #Descrição da função

            asct = False #Acesso Só Com Token

            if asct and (self.access_token == "" or self.access_token == None or type(self.access_token) != str):
                print("Token inválido")
                return {}

            url = self.base_url+f"/visits/items"

            # Se for uma lista, junta com vírgula, senão usa como string
            if isinstance(item_ids, list):
                ids_param = ','.join(item_ids)
            else:
                ids_param = item_ids

            params = {
                'ids': ids_param,
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
        
        def visitas_periodo(self, item_ids, date_from, date_to, **kwargs):
            """
            Visitas por anúncios entre intervalos de datas
            
            Args:
                item_ids: ID(s) do(s) anúncio(s) - pode ser string única ou lista
                date_from: Data de início (formato ISO: YYYY-MM-DD)
                date_to: Data de fim (formato ISO: YYYY-MM-DD)
            """
            
            asct = True #Acesso Só Com Token

            if asct and (self.access_token == "" or self.access_token == None or type(self.access_token) != str):
                print("Token inválido")
                return {}

            url = self.base_url+f"/items/visits"

            # Se for uma lista, junta com vírgula, senão usa como string
            if isinstance(item_ids, list):
                ids_param = ','.join(item_ids)
            else:
                ids_param = item_ids

            params = {
                'ids': ids_param,
                'date_from': date_from,
                'date_to': date_to,
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

            response = self.request("GET", url=url)

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

            params = {}

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

        def precos(self, item_id, **kwargs):
            """
            Descrição da função
            """
            #Descrição da função

            asct = True
            if asct and (self.access_token == "" or self.access_token == None or type(self.access_token) != str):
                print("Token inválido")
                return {}
            
            url = self.base_url+f"/items/{item_id}/sale_price"

            params = {}
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

        def qualidade_publicacao(self, mlb, **kwargs):
            """
            Pega a qualidade de publicação do anúncio
            """
            #Descrição da função

            asct = True #Acesso Só Com Token

            if asct and (self.access_token == "" or self.access_token == None or type(self.access_token) != str):
                print("Token inválido")
                return {}

            url = self.base_url+f"/item/{mlb}/performance"

            params = {}

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

            params = {}

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

    class put(auth):

        def editar(self, mlb, dados={}, **kwargs):
            """
            Descrição da função
            """
            #Descrição da função

            asct = False
            #Acesso Só Com Token

            if asct and (self.access_token == "" or self.access_token == None or type(self.access_token) != str):
                print("Token inválido")
                return {}
            
            url = self.base_url+f"/items/{mlb}"

            params = {}

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

            response = self.request("PUT", url=url, params=params, headers=headers, data=json.dumps(dados))

            if response:
                return response.json()
            else:
                return {}
            
        def editar_preco(self, mlb, preco, **kwargs):
            """
            Descrição da função
            """
            #Descrição da função

            asct = False
            #Acesso Só Com Token
            if asct and (self.access_token == "" or self.access_token == None or type(self.access_token) != str):
                print("Token inválido")
                return {}

            params = {}

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

            anuncio_atual = anuncio.get(self.access_token).unico(mlb)

            if anuncio_atual == {}:
                print("Anúncio não encontrado")
                return {}
            
            dados = {}
            
            if anuncio_atual['variations'] != []:
                dados['variations'] = []
                variacoes = anuncio_atual['variations']
                for variacao in variacoes:
                    dados['variations'].append({
                        'id': variacao['id'],
                        'price': preco
                    })
            else:
                dados['price'] = preco

            response = self.editar(mlb, dados=dados, **kwargs)
            
            if response:
                return response
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

        response = self.request("GET", url=url)

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

        response = self.request("GET", url=url)

        if response:

            return response.json()
        
        else:
            return {}
    
    def visitas_usuario(self, user_id, date_from, date_to, **kwargs):
        """
        Total de visitas por usuário entre datas
        
        Args:
            user_id: ID do usuário
            date_from: Data de início (formato ISO: YYYY-MM-DD)
            date_to: Data de fim (formato ISO: YYYY-MM-DD)
        """
        
        asct = True #Acesso Só Com Token

        if asct and (self.access_token == "" or self.access_token == None or type(self.access_token) != str):
            print("Token inválido")
            return {}

        url = self.base_url+f"/users/{user_id}/items_visits"

        params = {
            'date_from': date_from,
            'date_to': date_to,
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
    
    def visitas_usuario_periodo(self, user_id, last, unit, ending=None, **kwargs):
        """
        Visitantes por data por usuário em janela de tempo
        
        Args:
            user_id: ID do usuário
            last: Quantos períodos antes (ex: 30)
            unit: Unidade de tempo ("day")
            ending: Data de fim opcional (formato ISO: YYYY-MM-DD)
        """
        
        asct = True #Acesso Só Com Token

        if asct and (self.access_token == "" or self.access_token == None or type(self.access_token) != str):
            print("Token inválido")
            return {}

        url = self.base_url+f"/users/{user_id}/items_visits/time_window"

        params = {
            'last': last,
            'unit': unit,
        }

        if ending:
            params['ending'] = ending

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

                    response2 = self.request("GET", url=url, params=params)

                    for item in response2.json()['results']:
                        items.append(item)

            return items
        
        else:
            return []
        
    def sla_envio(self, shipment_id, **kwargs):
        """
        Descrição da função
        """
        #Descrição da função

        asct = True #Acesso Só Com Token

        if asct and (self.access_token == "" or self.access_token == None or type(self.access_token) != str):
            print("Token inválido")
            return []

        url = self.base_url+f"/shipments/{shipment_id}/sla"

        params = {}

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

        response = self.request("GET", url=url)

        if response:

            return response.json()
        
        else:
            return {}

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

        response = self.request("GET", url=url)

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

        response = self.request("GET", url=url)

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

        params = {}

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