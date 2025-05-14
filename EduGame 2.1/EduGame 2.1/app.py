from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
import random

app = Flask(__name__)
app.secret_key = os.urandom(24).hex()

# Diccionario que contiene las preguntas organizadas por materia y nivel de dificultad
quizzes = {
    'matematicas': {
        'facil': [
            {'id': 1, 'question': '¿Cuánto es 5 + 3?', 'options': ['6', '7', '8', '9'], 'correct': '8', 'explanation': '5 + 3 = 8, una suma básica.'},
            {'id': 2, 'question': '¿Cuál es el doble de 4?', 'options': ['6', '8', '10', '12'], 'correct': '8', 'explanation': 'El doble de 4 es 4 × 2 = 8.'},
            {'id': 3, 'question': '¿Cuánto es 10 - 4?', 'options': ['4', '5', '6', '7'], 'correct': '6', 'explanation': '10 - 4 = 6, una resta simple.'},
            {'id': 4, 'question': '¿Cuál es el resultado de 3 × 5?', 'options': ['12', '15', '18', '20'], 'correct': '15', 'explanation': '3 × 5 = 15, una multiplicación básica.'},
            {'id': 5, 'question': '¿Cuánto es 20 ÷ 4?', 'options': ['4', '5', '6', '7'], 'correct': '5', 'explanation': '20 ÷ 4 = 5, una división simple.'},
            {'id': 6, 'question': '¿Cuánto es 7 + 6?', 'options': ['11', '12', '13', '14'], 'correct': '13', 'explanation': '7 + 6 = 13, suma básica.'},
            {'id': 7, 'question': '¿Cuál es el triple de 3?', 'options': ['6', '9', '12', '15'], 'correct': '9', 'explanation': 'El triple de 3 es 3 × 3 = 9.'},
            {'id': 8, 'question': '¿Cuánto es 15 - 7?', 'options': ['6', '7', '8', '9'], 'correct': '8', 'explanation': '15 - 7 = 8, resta simple.'},
            {'id': 9, 'question': '¿Cuál es el resultado de 4 × 6?', 'options': ['20', '22', '24', '26'], 'correct': '24', 'explanation': '4 × 6 = 24, multiplicación básica.'},
            {'id': 10, 'question': '¿Cuánto es 18 ÷ 3?', 'options': ['5', '6', '7', '8'], 'correct': '6', 'explanation': '18 ÷ 3 = 6, división simple.'},
        ],
        'intermedio': [
            {'id': 11, 'question': 'Resuelve: 2x + 4 = 10', 'options': ['x=2', 'x=3', 'x=4', 'x=5'], 'correct': 'x=3', 'explanation': '2x + 4 = 10 → 2x = 6 → x = 3.'},
            {'id': 12, 'question': '¿Cuál es el área de un triángulo con base 6 y altura 4?', 'options': ['12', '18', '24', '30'], 'correct': '12', 'explanation': 'Área = (base × altura) ÷ 2 = (6 × 4) ÷ 2 = 12.'},
            {'id': 13, 'question': '¿Cuánto es 2³ + 3²?', 'options': ['15', '17', '19', '21'], 'correct': '17', 'explanation': '2³ = 8, 3² = 9, 8 + 9 = 17.'},
            {'id': 14, 'question': 'Resuelve: 5x - 10 = 15', 'options': ['x=3', 'x=4', 'x=5', 'x=6'], 'correct': 'x=5', 'explanation': '5x - 10 = 15 → 5x = 25 → x = 5.'},
            {'id': 15, 'question': '¿Cuál es el perímetro de un rectángulo de 5x3?', 'options': ['15', '16', '18', '20'], 'correct': '16', 'explanation': 'Perímetro = 2(largo + ancho) = 2(5 + 3) = 16.'},
            {'id': 16, 'question': '¿Cuánto es 4² - 2²?', 'options': ['10', '12', '14', '16'], 'correct': '12', 'explanation': '4² = 16, 2² = 4, 16 - 4 = 12.'},
            {'id': 17, 'question': 'Resuelve: 3x + 6 = 15', 'options': ['x=2', 'x=3', 'x=4', 'x=5'], 'correct': 'x=3', 'explanation': '3x + 6 = 15 → 3x = 9 → x = 3.'},
            {'id': 18, 'question': '¿Cuál es el área de un rectángulo de 8x5?', 'options': ['30', '35', '40', '45'], 'correct': '40', 'explanation': 'Área = largo × ancho = 8 × 5 = 40.'},
            {'id': 19, 'question': '¿Cuánto es 5³ ÷ 5?', 'options': ['20', '25', '30', '35'], 'correct': '25', 'explanation': '5³ = 125, 125 ÷ 5 = 25.'},
            {'id': 20, 'question': 'Resuelve: x² = 16', 'options': ['x=2', 'x=3', 'x=4', 'x=5'], 'correct': 'x=4', 'explanation': 'x² = 16 → x = ±4, pero en opciones solo está x=4.'},
        ],
        'dificil': [
            {'id': 21, 'question': '¿Cuál es el valor de x en 3x² - 12 = 0?', 'options': ['x=2', 'x=3', 'x=4', 'x=±2'], 'correct': 'x=±2', 'explanation': '3x² - 12 = 0 → x² = 4 → x = ±2.'},
            {'id': 22, 'question': 'Si sen(θ) = 0.6, ¿cuál es cos(θ)? (θ en primer cuadrante)', 'options': ['0.6', '0.8', '0.4', '1.0'], 'correct': '0.8', 'explanation': 'sen²(θ) + cos²(θ) = 1 → 0.6² + cos²(θ) = 1 → cos(θ) = 0.8.'},
            {'id': 23, 'question': 'Resuelve: log₂(8) = x', 'options': ['x=2', 'x=3', 'x=4', 'x=5'], 'correct': 'x=3', 'explanation': 'log₂(8) = x → 2^x = 8 → x = 3.'},
            {'id': 24, 'question': '¿Cuál es la derivada de x³?', 'options': ['x²', '2x', '3x²', '3x'], 'correct': '3x²', 'explanation': 'La derivada de x³ es 3x² por la regla de potencias.'},
            {'id': 25, 'question': '¿Cuál es el área de un círculo con radio 5?', 'options': ['25π', '20π', '15π', '10π'], 'correct': '25π', 'explanation': 'Área = πr² = π × 5² = 25π.'},
            {'id': 26, 'question': 'Resuelve: 2x² + 5x - 3 = 0', 'options': ['x=1, -3', 'x=1, -1.5', 'x=0.5, -3', 'x=0.5, -1.5'], 'correct': 'x=0.5, -3', 'explanation': 'Usando la fórmula cuadrática, x = [-5 ± √(25 + 24)] ÷ 4 = [1, -6] ÷ 2.'},
            {'id': 27, 'question': '¿Cuál es el valor de tan(45°)?', 'options': ['0', '1', '√2', '√3'], 'correct': '1', 'explanation': 'tan(45°) = sen(45°) ÷ cos(45°) = (√2/2) ÷ (√2/2) = 1.'},
            {'id': 28, 'question': '¿Cuál es la integral de 2x?', 'options': ['x²', '2x²', 'x² + C', '2x + C'], 'correct': 'x² + C', 'explanation': 'La integral de 2x es x² + C.'},
            {'id': 29, 'question': 'Resuelve: e^x = 1', 'options': ['x=0', 'x=1', 'x=2', 'x=-1'], 'correct': 'x=0', 'explanation': 'e^x = 1 → x = 0, ya que e^0 = 1.'},
            {'id': 30, 'question': '¿Cuál es el límite de (x² - 1)/(x - 1) cuando x → 1?', 'options': ['0', '1', '2', '3'], 'correct': '2', 'explanation': '(x² - 1)/(x - 1) = (x - 1)(x + 1)/(x - 1) = x + 1 → límite = 2.'},
        ]
    },
    'lenguaje': {
        'facil': [
            {'id': 31, 'question': '¿Cuál es un sinónimo de "feliz"?', 'options': ['Triste', 'Alegre', 'Cansado', 'Enojado'], 'correct': 'Alegre', 'explanation': '"Feliz" y "alegre" ambos describen un estado de alegría.'},
            {'id': 32, 'question': '¿Qué es un sustantivo?', 'options': ['Una acción', 'Un nombre', 'Una descripción', 'Un lugar'], 'correct': 'Un nombre', 'explanation': 'Un sustantivo nombra personas, lugares o cosas.'},
            {'id': 33, 'question': '¿Cuál es el antónimo de "grande"?', 'options': ['Pequeño', 'Alto', 'Largo', 'Ancho'], 'correct': 'Pequeño', 'explanation': '"Grande" y "pequeño" son opuestos en tamaño.'},
            {'id': 34, 'question': '¿Qué es un verbo?', 'options': ['Un lugar', 'Una acción', 'Un objeto', 'Una persona'], 'correct': 'Una acción', 'explanation': 'Un verbo describe acciones o estados.'},
            {'id': 35, 'question': '¿Cuál es el plural de "sol"?', 'options': ['Soles', 'Sol', 'Solas', 'Sole'], 'correct': 'Soles', 'explanation': 'El plural de "sol" es "soles".'},
            {'id': 36, 'question': '¿Cuál es un sinónimo de "rápido"?', 'options': ['Lento', 'Veloz', 'Pesado', 'Fuerte'], 'correct': 'Veloz', 'explanation': '"Rápido" y "veloz" indican alta velocidad.'},
            {'id': 37, 'question': '¿Qué es un adjetivo?', 'options': ['Una acción', 'Un nombre', 'Una descripción', 'Un lugar'], 'correct': 'Una descripción', 'explanation': 'Un adjetivo describe un sustantivo.'},
            {'id': 38, 'question': '¿Cuál es el antónimo de "claro"?', 'options': ['Oscuro', 'Brillante', 'Luminoso', 'Transparente'], 'correct': 'Oscuro', 'explanation': '"Claro" y "oscuro" son opuestos en luz.'},
            {'id': 39, 'question': '¿Cuál es el singular de "casas"?', 'options': ['Casa', 'Casas', 'Casi', 'Caso'], 'correct': 'Casa', 'explanation': 'El singular de "casas" es "casa".'},
            {'id': 40, 'question': '¿Qué es un pronombre?', 'options': ['Sustituye un nombre', 'Describe un verbo', 'Indica tiempo', 'Une oraciones'], 'correct': 'Sustituye un nombre', 'explanation': 'Un pronombre reemplaza a un sustantivo.'},
        ],
        'intermedio': [
            {'id': 41, 'question': 'Identifica la figura retórica: "El viento canta en la noche."', 'options': ['Metáfora', 'Personificación', 'Símil', 'Hipérbole'], 'correct': 'Personificación', 'explanation': 'El viento no canta, se le da una característica humana.'},
            {'id': 42, 'question': '¿Cuál es el pretérito perfecto de "correr"?', 'options': ['Corrí', 'He corrido', 'Corriendo', 'Correré'], 'correct': 'He corrido', 'explanation': 'El pretérito perfecto es "he corrido".'},
            {'id': 43, 'question': '¿Qué es un adjetivo?', 'options': ['Describe una acción', 'Describe un sustantivo', 'Indica lugar', 'Indica tiempo'], 'correct': 'Describe un sustantivo', 'explanation': 'Un adjetivo califica un sustantivo.'},
            {'id': 44, 'question': 'Identifica el sujeto en: "El perro corre rápido."', 'options': ['Corre', 'Rápido', 'El perro', 'Perro rápido'], 'correct': 'El perro', 'explanation': 'El sujeto realiza la acción: "el perro".'},
            {'id': 45, 'question': '¿Cuál es un sinónimo de "hermoso"?', 'options': ['Feo', 'Bonito', 'Triste', 'Rápido'], 'correct': 'Bonito', 'explanation': '"Hermoso" y "bonito" indican belleza.'},
            {'id': 46, 'question': '¿Qué es una metáfora?', 'options': ['Comparación directa', 'Repetición', 'Exageración', 'Sustitución'], 'correct': 'Comparación directa', 'explanation': 'Una metáfora compara sin usar "como".'},
            {'id': 47, 'question': '¿Cuál es el futuro de "cantar"?', 'options': ['Canté', 'Canto', 'Cantaré', 'He cantado'], 'correct': 'Cantaré', 'explanation': 'El futuro de "cantar" es "cantaré".'},
            {'id': 48, 'question': 'Identifica la figura retórica: "Es un león en la batalla."', 'options': ['Símil', 'Metáfora', 'Personificación', 'Hipérbole'], 'correct': 'Metáfora', 'explanation': 'Compara sin usar "como".'},
            {'id': 49, 'question': '¿Qué es un adverbio?', 'options': ['Describe un sustantivo', 'Modifica un verbo', 'Sustituye un nombre', 'Indica lugar'], 'correct': 'Modifica un verbo', 'explanation': 'Un adverbio modifica verbos, adjetivos, etc.'},
            {'id': 50, 'question': '¿Cuál es el participio de "vivir"?', 'options': ['Vivo', 'Vivido', 'Viviendo', 'Viví'], 'correct': 'Vivido', 'explanation': 'El participio de "vivir" es "vivido".'},
        ],
        'dificil': [
            {'id': 51, 'question': '¿Qué tipo de oración es: "Si estudias, aprobarás"?', 'options': ['Declarativa', 'Condicional', 'Exclamativa', 'Interrogativa'], 'correct': 'Condicional', 'explanation': 'Expresa una condición: si... entonces.'},
            {'id': 52, 'question': '¿Quién escribió "Cien años de soledad"?', 'options': ['Mario Vargas Llosa', 'Gabriel García Márquez', 'Julio Cortázar', 'Isabel Allende'], 'correct': 'Gabriel García Márquez', 'explanation': 'Es la obra maestra de García Márquez.'},
            {'id': 53, 'question': '¿Qué es una anáfora?', 'options': ['Repetición al inicio', 'Comparación', 'Exageración', 'Sustitución'], 'correct': 'Repetición al inicio', 'explanation': 'Repite palabras al inicio de frases.'},
            {'id': 54, 'question': '¿Cuál es el género de "La casa en Mango Street"?', 'options': ['Poesía', 'Novela', 'Ensayo', 'Drama'], 'correct': 'Novela', 'explanation': 'Es una novela de Sandra Cisneros.'},
            {'id': 55, 'question': '¿Qué significa "metonimia"?', 'options': ['Sustitución por relación', 'Exageración', 'Comparación', 'Personificación'], 'correct': 'Sustitución por relación', 'explanation': 'Sustituye un término por otro relacionado.'},
            {'id': 56, 'question': '¿Quién escribió "Don Quijote de la Mancha"?', 'options': ['Lope de Vega', 'Miguel de Cervantes', 'Garcilaso de la Vega', 'Calderón de la Barca'], 'correct': 'Miguel de Cervantes', 'explanation': 'Es la obra cumbre de Cervantes.'},
            {'id': 57, 'question': '¿Qué es un oxímoron?', 'options': ['Contradicción', 'Comparación', 'Repetición', 'Sustitución'], 'correct': 'Contradicción', 'explanation': 'Combina términos opuestos, como "silencio ensordecedor".'},
            {'id': 58, 'question': '¿Cuál es el tema principal de "El principito"?', 'options': ['Amor', 'Amistad', 'Aventura', 'Guerra'], 'correct': 'Amistad', 'explanation': 'Explora la amistad y los valores humanos.'},
            {'id': 59, 'question': '¿Qué es un hipérbaton?', 'options': ['Alteración del orden', 'Exageración', 'Repetición', 'Comparación'], 'correct': 'Alteración del orden', 'explanation': 'Cambia el orden natural de la frase.'},
            {'id': 60, 'question': '¿Quién escribió "Crimen y castigo"?', 'options': ['Fiódor Dostoyevski', 'León Tolstói', 'Antón Chéjov', 'Vladimir Nabokov'], 'correct': 'Fiódor Dostoyevski', 'explanation': 'Es una novela de Dostoyevski.'},
        ]
    },
    'historia': {
        'facil': [
            {'id': 61, 'question': '¿En qué año llegó Colón a América?', 'options': ['1492', '1453', '1519', '1607'], 'correct': '1492', 'explanation': 'Colón llegó a América en 1492.'},
            {'id': 62, 'question': '¿Quién fue el primer presidente de El Salvador?', 'options': ['Juan José Guzmán', 'Francisco Morazán', 'Rafael Zaldívar', 'Santiago González'], 'correct': 'Juan José Guzmán', 'explanation': 'Fue el primer presidente en 1844.'},
            {'id': 63, 'question': '¿Qué país colonizó El Salvador?', 'options': ['Francia', 'España', 'Inglaterra', 'Portugal'], 'correct': 'España', 'explanation': 'España colonizó El Salvador en el siglo XVI.'},
            {'id': 64, 'question': '¿En qué siglo ocurrió la independencia de El Salvador?', 'options': ['XVII', 'XVIII', 'XIX', 'XX'], 'correct': 'XIX', 'explanation': 'La independencia fue en 1821, siglo XIX.'},
            {'id': 65, 'question': '¿Qué es la independencia?', 'options': ['Unión con otro país', 'Libertad de un país', 'Guerra civil', 'Colonización'], 'correct': 'Libertad de un país', 'explanation': 'Independencia es la liberación del control extranjero.'},
            {'id': 66, 'question': '¿Quién descubrió América?', 'options': ['Vasco da Gama', 'Cristóbal Colón', 'Fernando Magallanes', 'Marco Polo'], 'correct': 'Cristóbal Colón', 'explanation': 'Colón llegó a América en 1492.'},
            {'id': 67, 'question': '¿En qué continente ocurrió la Revolución Francesa?', 'options': ['América', 'Asia', 'Europa', 'África'], 'correct': 'Europa', 'explanation': 'Ocurrió en Francia, Europa, en 1789.'},
            {'id': 68, 'question': '¿Qué era un virreinato?', 'options': ['Un reino', 'Una colonia', 'Un imperio', 'Una república'], 'correct': 'Una colonia', 'explanation': 'Era una división colonial española.'},
            {'id': 69, 'question': '¿En qué año comenzó la Primera Guerra Mundial?', 'options': ['1914', '1918', '1939', '1945'], 'correct': '1914', 'explanation': 'Comenzó en 1914 tras el asesinato de Francisco Fernando.'},
            {'id': 70, 'question': '¿Qué es una monarquía?', 'options': ['Gobierno de muchos', 'Gobierno de uno', 'Gobierno sin rey', 'Gobierno electo'], 'correct': 'Gobierno de uno', 'explanation': 'Es un gobierno liderado por un rey o reina.'},
        ],
        'intermedio': [
            {'id': 71, 'question': '¿Qué evento marcó el inicio de la Segunda Guerra Mundial?', 'options': ['Invasión de Polonia', 'Ataque a Pearl Harbor', 'Batalla de Stalingrado', 'Tratado de Versalles'], 'correct': 'Invasión de Polonia', 'explanation': 'Alemania invadió Polonia en 1939, iniciando la guerra.'},
            {'id': 72, 'question': '¿Qué civilización construyó Machu Picchu?', 'options': ['Azteca', 'Maya', 'Inca', 'Olmeca'], 'correct': 'Inca', 'explanation': 'Los incas construyeron Machu Picchu en el siglo XV.'},
            {'id': 73, 'question': '¿Quién lideró la independencia de El Salvador en 1821?', 'options': ['José Matías Delgado', 'Manuel José Arce', 'Francisco Morazán', 'Juan José Guzmán'], 'correct': 'José Matías Delgado', 'explanation': 'Delgado fue líder clave en 1821.'},
            {'id': 74, 'question': '¿Qué fue el Renacimiento?', 'options': ['Una guerra', 'Un movimiento cultural', 'Una revolución política', 'Una peste'], 'correct': 'Un movimiento cultural', 'explanation': 'Fue un movimiento cultural en los siglos XV-XVI.'},
            {'id': 75, 'question': '¿En qué año cayó el Muro de Berlín?', 'options': ['1985', '1989', '1991', '1995'], 'correct': '1989', 'explanation': 'El Muro cayó en 1989, marcando el fin de la Guerra Fría.'},
            {'id': 76, 'question': '¿Qué fue la Revolución Industrial?', 'options': ['Cambio político', 'Cambio tecnológico', 'Cambio religioso', 'Cambio cultural'], 'correct': 'Cambio tecnológico', 'explanation': 'Transformó la producción con máquinas en el siglo XVIII.'},
            {'id': 77, 'question': '¿Quién fue Simón Bolívar?', 'options': ['Líder independentista', 'Rey español', 'Emperador francés', 'Científico'], 'correct': 'Líder independentista', 'explanation': 'Lideró la independencia de varios países sudamericanos.'},
            {'id': 78, 'question': '¿Qué fue la Guerra de los Cien Años?', 'options': ['Conflicto religioso', 'Conflicto entre Francia e Inglaterra', 'Guerra civil', 'Guerra mundial'], 'correct': 'Conflicto entre Francia e Inglaterra', 'explanation': 'Duró de 1337 a 1453.'},
            {'id': 79, 'question': '¿En qué siglo ocurrió la peste negra?', 'options': ['XII', 'XIII', 'XIV', 'XV'], 'correct': 'XIV', 'explanation': 'Ocurrió en el siglo XIV, matando a millones.'},
            {'id': 80, 'question': '¿Qué fue el Tratado de Tordesillas?', 'options': ['División colonial', 'Fin de una guerra', 'Unión de reinos', 'Reforma religiosa'], 'correct': 'División colonial', 'explanation': 'Dividió América entre España y Portugal en 1494.'},
        ],
        'dificil': [
            {'id': 81, 'question': '¿Qué tratado puso fin a la Guerra de Independencia de EE.UU.?', 'options': ['Tratado de París', 'Tratado de Versalles', 'Tratado de Tordesillas', 'Tratado de Guadalupe Hidalgo'], 'correct': 'Tratado de París', 'explanation': 'Firmado en 1783, dio independencia a EE.UU.'},
            {'id': 82, 'question': '¿En qué año se firmaron los Acuerdos de Paz en El Salvador?', 'options': ['1986', '1992', '1996', '2000'], 'correct': '1992', 'explanation': 'Los acuerdos de 1992 pusieron fin a la guerra civil.'},
            {'id': 83, 'question': '¿Qué emperador unificó Japón en el siglo XVI?', 'options': ['Oda Nobunaga', 'Tokugawa Ieyasu', 'Toyotomi Hideyoshi', 'Minamoto Yoritomo'], 'correct': 'Oda Nobunaga', 'explanation': 'Nobunaga inició la unificación en el siglo XVI.'},
            {'id': 84, 'question': '¿Qué fue la Guerra Fría?', 'options': ['Conflicto directo', 'Tensión ideológica', 'Guerra nuclear', 'Revolución industrial'], 'correct': 'Tensión ideológica', 'explanation': 'Fue una rivalidad entre EE.UU. y la URSS sin combate directo.'},
            {'id': 85, 'question': '¿Quién fue Cleopatra?', 'options': ['Reina de Roma', 'Reina de Egipto', 'Emperatriz de Persia', 'Líder griega'], 'correct': 'Reina de Egipto', 'explanation': 'Cleopatra fue la última reina ptolemaica de Egipto.'},
            {'id': 86, 'question': '¿Qué fue la Reforma Protestante?', 'options': ['Movimiento político', 'Movimiento religioso', 'Movimiento científico', 'Movimiento militar'], 'correct': 'Movimiento religioso', 'explanation': 'Iniciada por Lutero en 1517, desafió a la Iglesia Católica.'},
            {'id': 87, 'question': '¿Quién fue el líder de la Revolución Rusa de 1917?', 'options': ['Lenin', 'Stalin', 'Trotsky', 'Kerensky'], 'correct': 'Lenin', 'explanation': 'Lenin lideró la revolución bolchevique.'},
            {'id': 88, 'question': '¿Qué fue el feudalismo?', 'options': ['Sistema político', 'Sistema económico', 'Sistema social', 'Sistema religioso'], 'correct': 'Sistema social', 'explanation': 'Organizó la sociedad medieval en jerarquías.'},
            {'id': 89, 'question': '¿En qué año comenzó la Revolución Cubana?', 'options': ['1945', '1953', '1961', '1970'], 'correct': '1953', 'explanation': 'Comenzó con el asalto al cuartel Moncada en 1953.'},
            {'id': 90, 'question': '¿Qué fue la Ilustración?', 'options': ['Movimiento artístico', 'Movimiento filosófico', 'Movimiento militar', 'Movimiento religioso'], 'correct': 'Movimiento filosófico', 'explanation': 'Promovió la razón y la ciencia en el siglo XVIII.'},
        ]
    },
    'ciencias': {
        'facil': [
            {'id': 91, 'question': '¿Qué planeta es conocido como el planeta rojo?', 'options': ['Júpiter', 'Marte', 'Venus', 'Mercurio'], 'correct': 'Marte', 'explanation': 'Marte tiene un color rojizo por el óxido de hierro.'},
            {'id': 92, 'question': '¿Qué gas es esencial para la respiración?', 'options': ['Oxígeno', 'Nitrógeno', 'Dióxido de carbono', 'Helio'], 'correct': 'Oxígeno', 'explanation': 'El oxígeno es necesario para la respiración humana.'},
            {'id': 93, 'question': '¿Qué es el agua en estado sólido?', 'options': ['Vapor', 'Hielo', 'Lluvia', 'Nieve'], 'correct': 'Hielo', 'explanation': 'El agua sólida es hielo.'},
            {'id': 94, 'question': '¿Cuántos planetas hay en el Sistema Solar?', 'options': ['7', '8', '9', '10'], 'correct': '8', 'explanation': 'Hay 8 planetas desde que Plutón fue reclasificado.'},
            {'id': 95, 'question': '¿Qué animal es un mamífero?', 'options': ['Cocodrilo', 'Serpiente', 'Delfín', 'Tortuga'], 'correct': 'Delfín', 'explanation': 'Los delfines son mamíferos marinos.'},
            {'id': 96, 'question': '¿Qué es la gravedad?', 'options': ['Fuerza de atracción', 'Fuerza de repulsión', 'Energía luminosa', 'Energía térmica'], 'correct': 'Fuerza de atracción', 'explanation': 'La gravedad atrae objetos hacia el centro de la Tierra.'},
            {'id': 97, 'question': '¿Qué órgano bombea sangre?', 'options': ['Cerebro', 'Corazón', 'Pulmón', 'Hígado'], 'correct': 'Corazón', 'explanation': 'El corazón bompea sangre al cuerpo.'},
            {'id': 98, 'question': '¿Qué es un átomo?', 'options': ['Una célula', 'Una partícula', 'Un gas', 'Un líquido'], 'correct': 'Una partícula', 'explanation': 'El átomo es la unidad básica de la materia.'},
            {'id': 99, 'question': '¿Qué color tiene el cloroformo?', 'options': ['Verde', 'Incoloro', 'Rojo', 'Azul'], 'correct': 'Incoloro', 'explanation': 'El cloroformo es un líquido incoloro.'},
            {'id': 100, 'question': '¿Qué es una planta?', 'options': ['Animal', 'Mineral', 'Vegetal', 'Gas'], 'correct': 'Vegetal', 'explanation': 'Las plantas son organismos vegetales.'},
        ],
        'intermedio': [
            {'id': 101, 'question': '¿Cuál es la fórmula del agua?', 'options': ['H₂O', 'CO₂', 'O₂', 'H₂SO₄'], 'correct': 'H₂O', 'explanation': 'El agua está compuesta por dos hidrógenos y un oxígeno.'},
            {'id': 102, 'question': '¿Qué tipo de energía se almacena en un resorte comprimido?', 'options': ['Cinética', 'Potencial', 'Térmica', 'Química'], 'correct': 'Potencial', 'explanation': 'La energía almacenada es potencial elástica.'},
            {'id': 103, 'question': '¿Qué es la fotosíntesis?', 'options': ['Respiración', 'Producción de alimento', 'Digestión', 'Circulación'], 'correct': 'Producción de alimento', 'explanation': 'Las plantas producen alimento usando luz solar.'},
            {'id': 104, 'question': '¿Cuál es el hueso más largo del cuerpo?', 'options': ['Fémur', 'Húmero', 'Tibia', 'Radio'], 'correct': 'Fémur', 'explanation': 'El fémur es el hueso más largo en el muslo.'},
            {'id': 105, 'question': '¿Qué mide un termómetro?', 'options': ['Presión', 'Temperatura', 'Humedad', 'Velocidad'], 'correct': 'Temperatura', 'explanation': 'Un termómetro mide la temperatura.'},
            {'id': 106, 'question': '¿Qué es un electrón?', 'options': ['Partícula positiva', 'Partícula negativa', 'Partícula neutra', 'Partícula pesada'], 'correct': 'Partícula negativa', 'explanation': 'El electrón tiene carga negativa.'},
            {'id': 107, 'question': '¿Qué es la densidad?', 'options': ['Masa por volumen', 'Peso por área', 'Volumen por masa', 'Fuerza por área'], 'correct': 'Masa por volumen', 'explanation': 'Densidad = masa ÷ volumen.'},
            {'id': 108, 'question': '¿Cuál es la unidad de la fuerza?', 'options': ['Joule', 'Newton', 'Watt', 'Pascal'], 'correct': 'Newton', 'explanation': 'La fuerza se mide en newtons.'},
            {'id': 109, 'question': '¿Qué es un ecosistema?', 'options': ['Un solo organismo', 'Una comunidad de organismos', 'Un mineral', 'Un gas'], 'correct': 'Una comunidad de organismos', 'explanation': 'Incluye organismos y su entorno.'},
            {'id': 110, 'question': '¿Qué es la mitosis?', 'options': ['División celular', 'Fusión celular', 'Digestión celular', 'Movimiento celular'], 'correct': 'División celular', 'explanation': 'La mitosis divide una célula en dos idénticas.'},
        ],
        'dificil': [
            {'id': 111, 'question': '¿Cuál es la unidad de medida de la resistencia eléctrica?', 'options': ['Voltio', 'Amperio', 'Ohmio', 'Watt'], 'correct': 'Ohmio', 'explanation': 'La resistencia se mide en ohmios.'},
            {'id': 112, 'question': '¿Qué científico propuso la teoría de la relatividad?', 'options': ['Isaac Newton', 'Albert Einstein', 'Galileo Galilei', 'Niels Bohr'], 'correct': 'Albert Einstein', 'explanation': 'Einstein propuso la relatividad en 1905 y 1915.'},
            {'id': 113, 'question': '¿Cuál es la carga del protón?', 'options': ['Negativa', 'Positiva', 'Neutra', 'Variable'], 'correct': 'Positiva', 'explanation': 'El protón tiene carga positiva.'},
            {'id': 114, 'question': '¿Qué es el ADN?', 'options': ['Proteína', 'Carbohidrato', 'Ácido nucleico', 'Lípido'], 'correct': 'Ácido nucleico', 'explanation': 'El ADN es un ácido nucleico que contiene genes.'},
            {'id': 115, 'question': '¿Qué gas es el más abundante en la atmósfera?', 'options': ['Oxígeno', 'Nitrógeno', 'Dióxido de carbono', 'Argón'], 'correct': 'Nitrógeno', 'explanation': 'El nitrógeno constituye ~78% de la atmósfera.'},
            {'id': 116, 'question': '¿Qué es la entropía?', 'options': ['Orden', 'Desorden', 'Energía', 'Masa'], 'correct': 'Desorden', 'explanation': 'La entropía mide el desorden en un sistema.'},
            {'id': 117, 'question': '¿Cuál es la velocidad de la luz?', 'options': ['300,000 km/s', '150,000 km/s', '600,000 km/s', '1,000 km/s'], 'correct': '300,000 km/s', 'explanation': 'La luz viaja a ~300,000 km/s en el vacío.'},
            {'id': 118, 'question': '¿Qué es la teoría del Big Bang?', 'options': ['Origen del universo', 'Origen de la Tierra', 'Origen de la vida', 'Origen de las galaxias'], 'correct': 'Origen del universo', 'explanation': 'Explica el inicio del universo hace ~13.8 mil millones de años.'},
            {'id': 119, 'question': '¿Qué es un agujero negro?', 'options': ['Estrella brillante', 'Región de gran gravedad', 'Planeta oscuro', 'Cometa'], 'correct': 'Región de gran gravedad', 'explanation': 'Su gravedad atrapa incluso la luz.'},
            {'id': 120, 'question': '¿Qué es la homeostasis?', 'options': ['Crecimiento', 'Equilibrio interno', 'Reproducción', 'Movimiento'], 'correct': 'Equilibrio interno', 'explanation': 'Mantiene condiciones estables en el cuerpo.'},
        ]
    },
    'cultura general': {
        'facil': [
            {'id': 121, 'question': '¿Cuál es la capital de Francia?', 'options': ['París', 'Londres', 'Madrid', 'Roma'], 'correct': 'París', 'explanation': 'París es la capital de Francia.'},
            {'id': 122, 'question': '¿De qué color es una esmeralda?', 'options': ['Rojo', 'Verde', 'Azul', 'Amarillo'], 'correct': 'Verde', 'explanation': 'La esmeralda es una gema verde.'},
            {'id': 123, 'question': '¿Cuántos continentes hay?', 'options': ['5', '6', '7', '8'], 'correct': '7', 'explanation': 'Hay 7 continentes habitados.'},
            {'id': 124, 'question': '¿Qué animal es el rey de la selva?', 'options': ['Tigre', 'León', 'Elefante', 'Jirafa'], 'correct': 'León', 'explanation': 'El león es conocido como el rey de la selva.'},
            {'id': 125, 'question': '¿Cuál es el océano más grande?', 'options': ['Atlántico', 'Índico', 'Pacífico', 'Ártico'], 'correct': 'Pacífico', 'explanation': 'El Pacífico es el océano más grande del mundo.'},
            {'id': 126, 'question': '¿Qué es el Sol?', 'options': ['Planeta', 'Estrella', 'Satélite', 'Cometa'], 'correct': 'Estrella', 'explanation': 'El Sol es una estrella en el centro del Sistema Solar.'},
            {'id': 127, 'question': '¿Cuál es la capital de El Salvador?', 'options': ['San Salvador', 'Santa Ana', 'San Miguel', 'Sonsonate'], 'correct': 'San Salvador', 'explanation': 'San Salvador es la capital de El Salvador.'},
            {'id': 128, 'question': '¿Cuántos días tiene un año bisiesto?', 'options': ['364', '365', '366', '367'], 'correct': '366', 'explanation': 'Un año bisiesto tiene 366 días.'},
            {'id': 129, 'question': '¿Qué es un volcán?', 'options': ['Montaña con lava', 'Lago profundo', 'Cueva subterránea', 'Río caliente'], 'correct': 'Montaña con lava', 'explanation': 'Un volcán expulsa lava y gases.'},
            {'id': 130, 'question': '¿Cuál es el idioma oficial de México?', 'options': ['Portugués', 'Español', 'Francés', 'Inglés'], 'correct': 'Español', 'explanation': 'El español es el idioma oficial de México.'},
        ],
        'intermedio': [
            {'id': 131, 'question': '¿En qué continente está Egipto?', 'options': ['Asia', 'África', 'Europa', 'Australia'], 'correct': 'África', 'explanation': 'Egipto está en el noreste de África.'},
            {'id': 132, 'question': '¿Qué instrumento toca un violinista?', 'options': ['Violín', 'Flauta', 'Trombón', 'Batería'], 'correct': 'Violín', 'explanation': 'Un violinista toca el violín.'},
            {'id': 133, 'question': '¿Quién pintó la Mona Lisa?', 'options': ['Pablo Picasso', 'Leonardo da Vinci', 'Vincent van Gogh', 'Claude Monet'], 'correct': 'Leonardo da Vinci', 'explanation': 'La Mona Lisa fue pintada por da Vinci.'},
            {'id': 134, 'question': '¿Qué idioma se habla en Brasil?', 'options': ['Español', 'Portugués', 'Francés', 'Inglés'], 'correct': 'Portugués', 'explanation': 'El portugués es el idioma oficial de Brasil.'},
            {'id': 135, 'question': '¿Cuál es la moneda de Japón?', 'options': ['Yuan', 'Yen', 'Won', 'Ringgit'], 'correct': 'Yen', 'explanation': 'El yen es la moneda de Japón.'},
            {'id': 136, 'question': '¿Qué es la ONU?', 'options': ['Organización deportiva', 'Organización internacional', 'Organización militar', 'Organización religiosa'], 'correct': 'Organización internacional', 'explanation': 'La ONU promueve la cooperación global.'},
            {'id': 137, 'question': '¿Cuál es el desierto más grande del mundo?', 'options': ['Sahara', 'Gobi', 'Antártico', 'Kalahari'], 'correct': 'Antártico', 'explanation': 'El desierto Antártico es el más grande por área.'},
            {'id': 138, 'question': '¿Qué es el Renacimiento?', 'options': ['Movimiento artístico', 'Guerra', 'Revolución política', 'Peste'], 'correct': 'Movimiento artístico', 'explanation': 'Fue un movimiento cultural y artístico en los siglos XV-XVI.'},
            {'id': 139, 'question': '¿Cuál es la capital de Australia?', 'options': ['Sydney', 'Melbourne', 'Canberra', 'Brisbane'], 'correct': 'Canberra', 'explanation': 'Canberra es la capital de Australia.'},
            {'id': 140, 'question': '¿Qué animal es el más rápido del mundo?', 'options': ['León', 'Guepardo', 'Águila', 'Caballo'], 'correct': 'Guepardo', 'explanation': 'El guepardo es el animal terrestre más rápido.'},
        ],
        'dificil': [
            {'id': 141, 'question': '¿En qué año se descubrió la penicilina?', 'options': ['1908', '1928', '1945', '1960'], 'correct': '1928', 'explanation': 'Alexander Fleming descubrió la penicilina en 1928.'},
            {'id': 142, 'question': '¿Qué filósofo escribió "El contrato social"?', 'options': ['John Locke', 'Jean-Jacques Rousseau', 'Immanuel Kant', 'Thomas Hobbes'], 'correct': 'Jean-Jacques Rousseau', 'explanation': 'Rousseau publicó "El contrato social" en 1762.'},
            {'id': 143, 'question': '¿Cuál es la montaña más alta del mundo?', 'options': ['K2', 'Kangchenjunga', 'Everest', 'Lhotse'], 'correct': 'Everest', 'explanation': 'El Monte Everest es la montaña más alta, con 8,848 metros.'},
            {'id': 144, 'question': '¿Qué país tiene más islas en el mundo?', 'options': ['Indonesia', 'Filipinas', 'Suecia', 'Japón'], 'correct': 'Suecia', 'explanation': 'Suecia tiene más de 220,000 islas.'},
            {'id': 145, 'question': '¿Quién compuso la Novena Sinfonía?', 'options': ['Mozart', 'Beethoven', 'Bach', 'Vivaldi'], 'correct': 'Beethoven', 'explanation': 'Ludwig van Beethoven compuso la Novena Sinfonía.'},
            {'id': 146, 'question': '¿Qué es el PIB?', 'options': ['Producto Interno Bruto', 'Plan Internacional de Bienestar', 'Programa de Inversión Básica', 'Producto Industrial Bruto'], 'correct': 'Producto Interno Bruto', 'explanation': 'El PIB mide la producción económica de un país.'},
            {'id': 147, 'question': '¿En qué año llegó el hombre a la Luna?', 'options': ['1965', '1969', '1972', '1975'], 'correct': '1969', 'explanation': 'El Apolo 11 llegó a la Luna en 1969.'},
            {'id': 148, 'question': '¿Qué es la UNESCO?', 'options': ['Organización de salud', 'Organización cultural', 'Organización militar', 'Organización económica'], 'correct': 'Organización cultural', 'explanation': 'La UNESCO promueve educación, ciencia y cultura.'},
            {'id': 149, 'question': '¿Cuál es el río más largo del mundo?', 'options': ['Amazonas', 'Nilo', 'Yangtsé', 'Misisipi'], 'correct': 'Amazonas', 'explanation': 'El Amazonas es el río más largo, con ~6,575 km.'},
            {'id': 150, 'question': '¿Qué pintor es conocido por "Las meninas"?', 'options': ['Goya', 'Velázquez', 'Picasso', 'Dalí'], 'correct': 'Velázquez', 'explanation': 'Diego Velázquez pintó "Las meninas" en 1656.'},
        ]
    }
}

materias = ['matematicas', 'lenguaje', 'historia', 'ciencias', 'cultura general']
niveles = ['facil', 'intermedio', 'dificil']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recursos')
def recursos():
    return render_template('recursos.html')

@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        if name and email and message:
            flash('¡Mensaje enviado con éxito! Nos pondremos en contacto pronto.', 'success')
        else:
            flash('Por favor, completa todos los campos.', 'error')
        return redirect(url_for('contacto'))
    return render_template('contacto.html')

@app.route('/sobre_nosotros')
def sobre_nosotros():
    return render_template('sobre_nosotros.html')

@app.route('/cuestionarios', methods=['GET', 'POST'])
def cuestionarios():
    materia = request.args.get('materia', 'matematicas')
    nivel = request.args.get('nivel', 'facil')
    if materia not in materias or nivel not in niveles:
        flash('Materia o nivel inválido.', 'error')
        return redirect(url_for('cuestionarios'))
    
    session_key = f'{materia}_{nivel}'
    if session_key not in session or request.form.get('action') == 'reset':
        session[session_key] = {
            'score': 0,
            'current_question': 0,
            'total_questions': 10,
            'questions': random.sample(quizzes[materia][nivel], min(10, len(quizzes[materia][nivel])))
        }
        if request.form.get('action') == 'reset':
            flash('Cuestionario reiniciado.', 'success')
    
    state = session[session_key]
    
    if request.method == 'POST' and 'answer' in request.form:
        answer = request.form.get('answer')
        try:
            question_id = int(request.form.get('question_id'))
            quiz = next((q for q in state['questions'] if q['id'] == question_id), None)
            if quiz and answer and 'correct' in quiz and quiz['correct']:
                if answer == quiz['correct']:
                    state['score'] += 10
                    flash(f'¡Correcto! {quiz["explanation"]}', 'success')
                else:
                    flash(f'Incorrecto. {quiz["explanation"]}', 'error')
                state['current_question'] += 1
                session[session_key] = state
                session.modified = True
            else:
                flash('Error: Pregunta o respuesta inválida.', 'error')
        except (ValueError, TypeError):
            flash('Error al procesar la respuesta. Por favor, intenta de nuevo.', 'error')
    
    if state['current_question'] >= state['total_questions']:
        percentage = (state['score'] / (state['total_questions'] * 10)) * 100
        badge = None
        if percentage >= 90:
            badge = "Maestro del Saber"
        elif percentage >= 70:
            badge = "Aprendiz Avanzado"
        elif percentage >= 50:
            badge = "Explorador del Conocimiento"
        return render_template('quiz_results.html', score=state['score'], total=state['total_questions'] * 10,
                               percentage=percentage, materia=materia, nivel=nivel, badge=badge)
    
    quiz = state['questions'][state['current_question']]
    # Verificar que quiz.correct sea válido antes de renderizar
    if not quiz or 'correct' not in quiz or not quiz['correct']:
        flash('Error: Pregunta inválida.', 'error')
        return redirect(url_for('cuestionarios', materia=materia, nivel=nivel))
    
    return render_template('cuestionarios.html', materias=materias, niveles=niveles, selected_materia=materia,
                           selected_nivel=nivel, score=state['score'], question_number=state['current_question'] + 1,
                           total_questions=state['total_questions'], quiz=quiz)

if __name__ == '__main__':
    app.run(debug=True)