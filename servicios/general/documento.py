from general.models.archivo import GenArchivo
from utilidades.utilidades import Utilidades
from utilidades.backblaze import Backblaze
from general.models.documento import GenDocumento
import requests
import json


class DocumentoServicio():

    @staticmethod
    def generar_cufe(documento: GenDocumento):                                                   
        cufe = 'Hola mundo'

        '''$emisor = [
            'numero_identificacion' => $arDocumento->getCuenta()->getNumeroIdentificacion(),
            'nombre' => $arDocumento->getCuenta()->getNombre()
        ];
        $adquiriente = $documento['adquiriente'];
        numero_completo = 
        
        $datosCufe = [
            'NumFac' => $numeroCompleto,
            'FecFac' => $documento['fecha'],
            'HorFac' => $documento['hora'],
            'ValFac' => $documento['subtotal'],
            'CodImp1' => "01",
            'ValImp1' => $documento['total_iva'],
            'CodImp2' => "04",
            'ValImp2' => $documento['total_consumo'],
            'CodImp3' => "03",
            'ValImp3' => $documento['total_ica'],
            'ValTotFac' => $documento['total_documento'],
            'NitOFE' => $emisor['numero_identificacion'],
            'NumAdq' => $adquiriente['numero_identificacion'],
            'ClTec' => $claveTecnica,
            'TipoAmbiente' => $documento['ambiente']
        ];
        $cufe = $datosCufe['NumFac'].$datosCufe['FecFac'].$datosCufe['HorFac'].$datosCufe['ValFac'].$datosCufe['CodImp1'].$datosCufe['ValImp1'].$datosCufe['CodImp2'].$datosCufe['ValImp2'].$datosCufe['CodImp3'].$datosCufe['ValImp3'].$datosCufe['ValTotFac'].$datosCufe['NitOFE'].$datosCufe['NumAdq'].$datosCufe['ClTec'].$datosCufe['TipoAmbiente'];
        $UUID = hash('sha384', $cufe);
        $QRCode = "NroFactura={$numeroCompleto} NitFacturador={$emisor['numero_identificacion']} NitAdquiriente={$adquiriente['numero_identificacion']} FechaFactura={$documento['fecha']} ValorTotalFactura={$documento['total_documento']} Cufe={$UUID} URL=https://catalogo-vpfe-hab.dian.gov.co/Document/FindDocument?documentKey={$UUID};partitionKey=co|06|94;emissionDate=20190620";
        $softwareSecurityCode = hash('sha384',$softwareID."12345".$numeroCompleto);'''


        return cufe                          