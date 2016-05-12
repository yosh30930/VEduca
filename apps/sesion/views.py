from django.db import IntegrityError, transaction
from django.http import HttpResponseRedirect
from django.views.generic import View, TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.views import login
from django import forms
# from django.core.urlresolvers import reverse
# Create your views here.
from apps.usuarios.models import Usuario, Pais, Institucion
from apps.actividades.models import Encuentro, Foro, Seminario, Panel, Espacio

from .forms import UsuarioResetForm

class InicioSesionView(View):
    def get(self, request, *args, **kwargs):
        ResetPruebas()
        if request.user.is_authenticated():
        #   return HttpResponseRedirect(reverse('login'))
            return HttpResponseRedirect('/inicio/')
        else:
            template_name = 'sesion/inicio_sesion.html'
            return login(request, *args, template_name=template_name, **kwargs)

    def post(self, request, *args, **kwargs):
        template_name = 'sesion/inicio_sesion.html'
        return login(request, *args, template_name=template_name, **kwargs)


class UsuarioResetView(FormView):
    """
    Vista donde se muestran todos los encuentros sobre los que el usuario
    tiene privilegios
    """
    template_name = "sesion/restaura_contrasena.html"
    form_class = UsuarioResetForm
    success_url = "/restaurar_contraseña_hecho/"


@transaction.atomic
def crea_actividad(Modelo, nombre, padre, *args, **kwargs):
    try:
        with transaction.atomic():
            actividad = Modelo(nombre=nombre, *args, **kwargs)
            actividad.save(padre=padre)
            return actividad
    except IntegrityError as e:
        raise e


def ResetPruebas():
    if len(Pais.objects.all()) == 0:
        ResetPais()
    if len(Institucion.objects.all()) == 0:
        ResetInstitucion()
    if len(Usuario.objects.all()) == 0:
        ResetUsuarios()
    if len(Encuentro.objects.all()) == 0:
        ResetActividades()
    if len(Espacio.objects.all()) == 0:
        ResetEspacios()


def ResetActividades():
    modelos = [Encuentro, Foro, Seminario, Panel]
    for modelo in modelos:
        modelo.objects.all().delete()
    encuentro = Encuentro.objects.create(nombre="Encuentro Internacional 2016 Costa Rica")
    foro1 = crea_actividad(
        Foro, "Educación Superior, Innovación e Internacionalización", encuentro,
        nombre_corto="Educación Superior")
    foro2 = crea_actividad(
        Foro, "Investigación, Desarrollo e Innovación (I+D+i) ", encuentro,
        nombre_corto="(I+D+i) ")
    seminario11 = crea_actividad(
        Seminario, "Programa Piloto Inclusión Digital, Estrategia Digital\
        Nacional, Gobierno de México", foro1)
    seminario21 = crea_actividad(
        Seminario, "Programa Piloto de Inclusión Digital, Estrategia Digital\
        Nacional, Gobierno de México", foro2)
    for idx in range(3):
        crea_actividad(Panel, "Panel 1." + str(idx), seminario11)
    for idx in range(3):
        crea_actividad(Panel, "Panel 2." + str(idx), seminario21)
    return


def ResetUsuarios():
    Usuario.objects.all().delete()
    Usuario.objects.create_superuser('sainoba@gmail.com', nombres='Marco Nila', contrasena='bar')
    Usuario.objects.create_user('mabruka8@mailinator.com', nombres='Alejandro Llovet', contrasena='bar')
    Usuario.objects.create_user('mabruka1@mailinator.com', nombres='Fernando Gamboa', contrasena='bar')
    Usuario.objects.create_user('mabruka2@mailinator.com', nombres='Elena García', contrasena='bar')
    Usuario.objects.create_user('mabruka3@mailinator.com', nombres='Pedro Rocha', contrasena='bar')
    Usuario.objects.create_user('mabruka4@mailinator.com', nombres='Juan Luis Valdés', contrasena='bar')
    Usuario.objects.create_user('mabruka5@mailinator.com', nombres='Julieta Palma', contrasena='bar')
    Usuario.objects.create_user('mabruka6@mailinator.com', nombres='Juan Manuel Valdés', contrasena='bar')
    Usuario.objects.create_user('mabruka7@mailinator.com', nombres='Luis Andrés Ochoa', contrasena='bar')


def ResetEspacios():
    return
    Espacio.objects.all().delete()
    encuentros = Encuentro.objects.all()
    idx = 1
    for encuentro in encuentros:
        for _ in range(10):
            nombre = "Espacio " + str(idx)
            Espacio(nombre=nombre, encuentro=encuentro).save()
            idx += 1


def ResetInstitucion():
    Institucion.objects.all().delete()
    pais = Pais.objects.get(id="MX")
    Institucion.objects.create(
        nombre="Universidad Nacional Autonoma de Mexico", nombre_corto="UNAM",
        pais=pais)
    pais = Pais.objects.get(id="US")
    Institucion.objects.create(
        nombre="Organización de los Estados Americanos", nombre_corto="OEA",
        pais=pais)
    pais = Pais.objects.get(id="CA")
    Institucion.objects.create(nombre="Google", pais=pais)


def ResetPais():
    Pais.objects.all().delete()
    Pais.objects.create(id='', nombre='Otro')
    Pais.objects.create(id='AF', nombre='Afganistán')
    Pais.objects.create(id='AL', nombre='Albania')
    Pais.objects.create(id='DE', nombre='Alemania')
    Pais.objects.create(id='AD', nombre='Andorra')
    Pais.objects.create(id='AO', nombre='Angola')
    Pais.objects.create(id='AI', nombre='Anguila')
    Pais.objects.create(id='AQ', nombre='Antártida')
    Pais.objects.create(id='AG', nombre='Antigua y Barbuda')
    Pais.objects.create(id='AN', nombre='Antillas Neerlandesas')
    Pais.objects.create(id='SA', nombre='Arabia Saudí')
    Pais.objects.create(id='DZ', nombre='Argelia')
    Pais.objects.create(id='AR', nombre='Argentina')
    Pais.objects.create(id='AM', nombre='Armenia')
    Pais.objects.create(id='AW', nombre='Aruba')
    Pais.objects.create(id='AU', nombre='Australia')
    Pais.objects.create(id='AT', nombre='Austria')
    Pais.objects.create(id='AZ', nombre='Azerbaiyán')
    Pais.objects.create(id='BE', nombre='Bélgica')
    Pais.objects.create(id='BS', nombre='Bahamas')
    Pais.objects.create(id='BH', nombre='Bahráin')
    Pais.objects.create(id='BD', nombre='Bangladesh')
    Pais.objects.create(id='BB', nombre='Barbados')
    Pais.objects.create(id='BZ', nombre='Belice')
    Pais.objects.create(id='BJ', nombre='Benín')
    Pais.objects.create(id='BM', nombre='Bermudas')
    Pais.objects.create(id='BY', nombre='Bielorrusia')
    Pais.objects.create(id='MM', nombre='Birmania; Myanmar')
    Pais.objects.create(id='BO', nombre='Bolivia')
    Pais.objects.create(id='BA', nombre='Bosnia y Hercegovina')
    Pais.objects.create(id='BW', nombre='Botsuana')
    Pais.objects.create(id='BR', nombre='Brasil')
    Pais.objects.create(id='BN', nombre='Brunéi')
    Pais.objects.create(id='BG', nombre='Bulgaria')
    Pais.objects.create(id='BF', nombre='Burkina Faso')
    Pais.objects.create(id='BI', nombre='Burundi')
    Pais.objects.create(id='BT', nombre='Bután')
    Pais.objects.create(id='CV', nombre='Cabo Verde')
    Pais.objects.create(id='KH', nombre='Camboya')
    Pais.objects.create(id='CM', nombre='Camerún')
    Pais.objects.create(id='CA', nombre='Canadá')
    Pais.objects.create(id='TD', nombre='Chad')
    Pais.objects.create(id='CL', nombre='Chile')
    Pais.objects.create(id='CN', nombre='China')
    Pais.objects.create(id='CY', nombre='Chipre')
    Pais.objects.create(id='CO', nombre='Colombia')
    Pais.objects.create(id='KM', nombre='Comoras')
    Pais.objects.create(id='CG', nombre='Congo')
    Pais.objects.create(id='KP', nombre='Corea del Norte')
    Pais.objects.create(id='KR', nombre='Corea del Sur')
    Pais.objects.create(id='CR', nombre='Costa Rica')
    Pais.objects.create(id='CI', nombre='Costa de Marfil')
    Pais.objects.create(id='HR', nombre='Croacia')
    Pais.objects.create(id='CU', nombre='Cuba')
    Pais.objects.create(id='DK', nombre='Dinamarca')
    Pais.objects.create(id='DM', nombre='Dominica')
    Pais.objects.create(id='EC', nombre='Ecuador')
    Pais.objects.create(id='EG', nombre='Egipto')
    Pais.objects.create(id='SV', nombre='El Salvador')
    Pais.objects.create(id='VA', nombre='El Vaticano')
    Pais.objects.create(id='AE', nombre='Emiratos Árabes Unidos')
    Pais.objects.create(id='ER', nombre='Eritrea')
    Pais.objects.create(id='SK', nombre='Eslovaquia')
    Pais.objects.create(id='SI', nombre='Eslovenia')
    Pais.objects.create(id='ES', nombre='España')
    Pais.objects.create(id='US', nombre='Estados Unidos')
    Pais.objects.create(id='EE', nombre='Estonia')
    Pais.objects.create(id='ET', nombre='Etiopía')
    Pais.objects.create(id='PH', nombre='Filipinas')
    Pais.objects.create(id='FI', nombre='Finlandia')
    Pais.objects.create(id='FJ', nombre='Fiyi')
    Pais.objects.create(id='FR', nombre='Francia')
    Pais.objects.create(id='GA', nombre='Gabón')
    Pais.objects.create(id='GM', nombre='Gambia')
    Pais.objects.create(id='GE', nombre='Georgia')
    Pais.objects.create(id='GH', nombre='Ghana')
    Pais.objects.create(id='GI', nombre='Gibraltar')
    Pais.objects.create(id='GD', nombre='Granada')
    Pais.objects.create(id='GR', nombre='Grecia')
    Pais.objects.create(id='GL', nombre='Groenlandia')
    Pais.objects.create(id='GP', nombre='Guadalupe')
    Pais.objects.create(id='GU', nombre='Guam')
    Pais.objects.create(id='GT', nombre='Guatemala')
    Pais.objects.create(id='GF', nombre='Guayana Francesa')
    Pais.objects.create(id='GN', nombre='Guinea')
    Pais.objects.create(id='GQ', nombre='Guinea Ecuatorial')
    Pais.objects.create(id='GW', nombre='Guinea-Bissau')
    Pais.objects.create(id='GY', nombre='Guyana')
    Pais.objects.create(id='HT', nombre='Haití')
    Pais.objects.create(id='HN', nombre='Honduras')
    Pais.objects.create(id='HK', nombre='Hong Kong')
    Pais.objects.create(id='HU', nombre='Hungría')
    Pais.objects.create(id='IN', nombre='India (la)')
    Pais.objects.create(id='ID', nombre='Indonesia')
    Pais.objects.create(id='IR', nombre='Irán')
    Pais.objects.create(id='IQ', nombre='Iraq')
    Pais.objects.create(id='IE', nombre='Irlanda')
    Pais.objects.create(id='BV', nombre='Isla Bouvet')
    Pais.objects.create(id='CX', nombre='Isla Christmas')
    Pais.objects.create(id='NF', nombre='Isla Norfolk')
    Pais.objects.create(id='IS', nombre='Islandia')
    Pais.objects.create(id='KY', nombre='Islas Caimán')
    Pais.objects.create(id='CC', nombre='Islas Cocos')
    Pais.objects.create(id='CK', nombre='Islas Cook')
    Pais.objects.create(id='FO', nombre='Islas Feroe')
    Pais.objects.create(id='GS',
                        nombre='Islas Georgia del Sur y Sandwich del Sur')
    Pais.objects.create(id='HM', nombre='Islas Heard y McDonald')
    Pais.objects.create(id='FK', nombre='Islas Malvinas')
    Pais.objects.create(id='MP', nombre='Islas Marianas del Norte')
    Pais.objects.create(id='MH', nombre='Islas Marshall')
    Pais.objects.create(id='PN', nombre='Islas Pitcairn')
    Pais.objects.create(id='SB', nombre='Islas Salomón')
    Pais.objects.create(id='TC', nombre='Islas Turcas y Caicos')
    Pais.objects.create(id='VI', nombre='Islas Vírgenes Americanas')
    Pais.objects.create(id='VG', nombre='Islas Vírgenes Británicas')
    Pais.objects.create(id='UM',
                        nombre='Islas menores alejadas de los Estados Unidos')
    Pais.objects.create(id='IL', nombre='Israel')
    Pais.objects.create(id='IT', nombre='Italia')
    Pais.objects.create(id='JM', nombre='Jamaica')
    Pais.objects.create(id='JP', nombre='Japón')
    Pais.objects.create(id='JO', nombre='Jordania')
    Pais.objects.create(id='KZ', nombre='Kazajistán')
    Pais.objects.create(id='KE', nombre='Kenia')
    Pais.objects.create(id='KG', nombre='Kirguizistán')
    Pais.objects.create(id='KI', nombre='Kiribati')
    Pais.objects.create(id='KW', nombre='Kuwait')
    Pais.objects.create(id='LB', nombre='Líbano')
    Pais.objects.create(id='LA', nombre='Laos')
    Pais.objects.create(id='LS', nombre='Lesoto')
    Pais.objects.create(id='LV', nombre='Letonia')
    Pais.objects.create(id='LR', nombre='Liberia')
    Pais.objects.create(id='LY', nombre='Libia')
    Pais.objects.create(id='LI', nombre='Liechtenstein')
    Pais.objects.create(id='LT', nombre='Lituania')
    Pais.objects.create(id='LU', nombre='Luxemburgo')
    Pais.objects.create(id='MX', nombre='México')
    Pais.objects.create(id='MC', nombre='Mónaco')
    Pais.objects.create(id='MO', nombre='Macao')
    Pais.objects.create(id='MK', nombre='Macedonia')
    Pais.objects.create(id='MG', nombre='Madagascar')
    Pais.objects.create(id='ML', nombre='Malí')
    Pais.objects.create(id='MY', nombre='Malasia')
    Pais.objects.create(id='MW', nombre='Malaui')
    Pais.objects.create(id='MV', nombre='Maldivas')
    Pais.objects.create(id='MT', nombre='Malta')
    Pais.objects.create(id='MA', nombre='Marruecos')
    Pais.objects.create(id='MQ', nombre='Martinica')
    Pais.objects.create(id='MU', nombre='Mauricio')
    Pais.objects.create(id='MR', nombre='Mauritania')
    Pais.objects.create(id='YT', nombre='Mayotte')
    Pais.objects.create(id='FM', nombre='Micronesia')
    Pais.objects.create(id='MD', nombre='Moldavia')
    Pais.objects.create(id='MN', nombre='Mongolia')
    Pais.objects.create(id='MS', nombre='Montserrat')
    Pais.objects.create(id='MZ', nombre='Mozambique')
    Pais.objects.create(id='NE', nombre='Níger')
    Pais.objects.create(id='NA', nombre='Namibia')
    Pais.objects.create(id='NR', nombre='Nauru')
    Pais.objects.create(id='NP', nombre='Nepal')
    Pais.objects.create(id='NI', nombre='Nicaragua')
    Pais.objects.create(id='NG', nombre='Nigeria')
    Pais.objects.create(id='NU', nombre='Niue')
    Pais.objects.create(id='NO', nombre='Noruega')
    Pais.objects.create(id='NC', nombre='Nueva Caledonia')
    Pais.objects.create(id='NZ', nombre='Nueva Zelanda')
    Pais.objects.create(id='OM', nombre='Omán')
    Pais.objects.create(id='NL', nombre='Países Bajos')
    Pais.objects.create(id='PK', nombre='Pakistán')
    Pais.objects.create(id='PW', nombre='Palaos')
    Pais.objects.create(id='PA', nombre='Panamá')
    Pais.objects.create(id='PG', nombre='Papúa-Nueva Guinea')
    Pais.objects.create(id='PY', nombre='Paraguay')
    Pais.objects.create(id='PE', nombre='Perú')
    Pais.objects.create(id='PF', nombre='Polinesia Francesa')
    Pais.objects.create(id='PL', nombre='Polonia')
    Pais.objects.create(id='PT', nombre='Portugal')
    Pais.objects.create(id='PR', nombre='Puerto Rico')
    Pais.objects.create(id='QA', nombre='Qatar')
    Pais.objects.create(id='GB', nombre='Reino Unido')
    Pais.objects.create(id='CF', nombre='República Centroafricana')
    Pais.objects.create(id='CZ', nombre='República Checa; Chequia')
    Pais.objects.create(id='CD', nombre='República Democrática del Congo')
    Pais.objects.create(id='DO', nombre='República Dominicana')
    Pais.objects.create(id='RE', nombre='Reunión')
    Pais.objects.create(id='RW', nombre='Ruanda')
    Pais.objects.create(id='RO', nombre='Rumania; Rumanía')
    Pais.objects.create(id='RU', nombre='Rusia')
    Pais.objects.create(id='EH', nombre='Sáhara Occidental')
    Pais.objects.create(id='WS', nombre='Samoa')
    Pais.objects.create(id='AS', nombre='Samoa Americana')
    Pais.objects.create(id='KN', nombre='San Cristóbal y Nieves')
    Pais.objects.create(id='SM', nombre='San Marino')
    Pais.objects.create(id='PM', nombre='San Pedro y Miquelón')
    Pais.objects.create(id='VC', nombre='San Vicente y las Granadinas')
    Pais.objects.create(id='SH', nombre='Santa Helena')
    Pais.objects.create(id='LC', nombre='Santa Lucía')
    Pais.objects.create(id='ST', nombre='Santo Tomé y Príncipe')
    Pais.objects.create(id='SN', nombre='Senegal')
    Pais.objects.create(id='SC', nombre='Seychelles')
    Pais.objects.create(id='SL', nombre='Sierra Leona')
    Pais.objects.create(id='SG', nombre='Singapur')
    Pais.objects.create(id='SY', nombre='Siria')
    Pais.objects.create(id='SO', nombre='Somalia')
    Pais.objects.create(id='LK', nombre='Sri Lanka')
    Pais.objects.create(id='SZ', nombre='Suazilandia')
    Pais.objects.create(id='ZA', nombre='Sudáfrica')
    Pais.objects.create(id='SD', nombre='Sudán')
    Pais.objects.create(id='SE', nombre='Suecia')
    Pais.objects.create(id='CH', nombre='Suiza')
    Pais.objects.create(id='SR', nombre='Surinam')
    Pais.objects.create(id='SJ', nombre='Svalbard y Jan Mayen')
    Pais.objects.create(id='TN', nombre='Túnez')
    Pais.objects.create(id='TH', nombre='Tailandia')
    Pais.objects.create(id='TW', nombre='Taiwán')
    Pais.objects.create(id='TZ', nombre='Tanzania')
    Pais.objects.create(id='TJ', nombre='Tayikistán')
    Pais.objects.create(id='IO', nombre='Territorio Británico del Océano Indico')
    Pais.objects.create(id='TF', nombre='Territorios Australes Franceses')
    Pais.objects.create(id='TL', nombre='Timor Oriental')
    Pais.objects.create(id='TG', nombre='Togo')
    Pais.objects.create(id='TK', nombre='Tokelau')
    Pais.objects.create(id='TO', nombre='Tonga')
    Pais.objects.create(id='TT', nombre='Trinidad y Tobago')
    Pais.objects.create(id='TM', nombre='Turkmenistán')
    Pais.objects.create(id='TR', nombre='Turquía')
    Pais.objects.create(id='TV', nombre='Tuvalu')
    Pais.objects.create(id='UA', nombre='Ucrania')
    Pais.objects.create(id='UG', nombre='Uganda')
    Pais.objects.create(id='UY', nombre='Uruguay')
    Pais.objects.create(id='UZ', nombre='Uzbekistán')
    Pais.objects.create(id='VU', nombre='Vanuatu')
    Pais.objects.create(id='VE', nombre='Venezuela')
    Pais.objects.create(id='VN', nombre='Vietnam')
    Pais.objects.create(id='WF', nombre='Wallis y Futuna')
    Pais.objects.create(id='YE', nombre='Yemen')
    Pais.objects.create(id='DJ', nombre='Yibuti')
    Pais.objects.create(id='YU', nombre='Yugoslavia')
    Pais.objects.create(id='ZM', nombre='Zambia')
    Pais.objects.create(id='ZW', nombre='Zimbabue')
