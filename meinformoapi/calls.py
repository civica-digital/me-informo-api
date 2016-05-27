import requests

def entities(state = None, sector = None):
    r = requests.get("http://www.plataformadetransparencia.org.mx/map-portlet/js/entidades.json")
    response = r.json()
    data_output = []
    for state_data in response["Estado"]:
        for sector_data in state_data["sectores"]:
            for subject_data in sector_data["sujetos"]:
                subject_data["estado"] = state_data["nombre"]
                subject_data["sector"] = sector_data["nombre"]
                data_output.append(subject_data)
    return data_output

def foi_search(query,page = 1,resultspage = 25):
    r = requests.post('http://esbmx.inai.org.mx:8080/infomex/busqueda/solicitudes', data = {'cadenaBusqueda':str(query),'tamanioPagina':str(resultspage), "numeroPagina":str(page)})
    response_data = r.json()
    output_dict = {}
    output_dict["total_results"] = response_data["numeroResultados"]
    output_dict["data"] = response_data["listaResultados"]
    output_dict["page"] = page
    output_dict["max_results"] = str(5000) #Given by observation of the api
    return output_dict
