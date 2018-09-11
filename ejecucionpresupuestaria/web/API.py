import requests
class Api:
    url = 'http://localhost:51543/'

    def validarToken(self, token):
        customHeaders = {'Authorization': 'Bearer ' + token}
        response = requests.get(self.url + 'api/usuarios', headers = customHeaders)
        if(response.status_code == requests.codes.ok):
            return response.json()

        return False

    def getToken(self, usuario, password):
        postdata = {'grant_type': 'password', 'username': usuario,
                   'password': password}

        response = requests.post(self.url + 'token', data=postdata)
        json = response.json()

        if(response.status_code == requests.codes.ok):
            return json["access_token"]

        return None

    def getUsuario(self, token):
        customHeaders = {'Authorization': 'Bearer ' + token}
        response = requests.get(self.url + 'api/usuarios/GetUsuario', headers = customHeaders)

        if(response.status_code == requests.codes.ok):
            return response.json()

        return None

    def leerDependencias(self, token):
        customHeaders = {'Authorization': 'Bearer ' + token}
        response = requests.get(self.url + 'api/dependencias', headers = customHeaders)
        if(response.status_code == requests.codes.ok):
            return response.json()

        return None

    def ejecucionPresupuestaria(self, idDependencia, token):
        customHeaders = {'Authorization': 'Bearer ' + token}
        response = requests.get(self.url + 'api/dependencias/EjecucionPresupuestaria/' + str(idDependencia), headers = customHeaders)
        if(response.status_code == requests.codes.ok):
            return response.json()

        return None

    def buscarFiltro(self, idDependencia, filtro, token):
        customHeaders = {'Authorization': 'Bearer ' + token}
        response = requests.get(self.url + 'api/dependencias/BuscarFiltro/' + str(idDependencia) + ", " + filtro, headers = customHeaders)
        if(response.status_code == requests.codes.ok):
            return response.json()

        return None

    def consultaConFiltros(self, idDependencia, filtro, token):
        customHeaders = {'Authorization': 'Bearer ' + token}
        response = requests.get(self.url + 'api/dependencias/EjecucionPresupuestariaFiltros/' + str(idDependencia) + ", " + str(filtro), headers = customHeaders)
        if(response.status_code == requests.codes.ok):
            return response.json()

        return None
