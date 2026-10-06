"""
================================================================
BLADE 
================================================================

Historia:
Un cazarecompensas llamado Blade es contratado para investigar
un castillo en medio de la nada. Al entrar descubre que está
lleno de vampiros. Solo su espada y sus habilidades le
permitirán sobrevivir y escapar.

Controles: se usan números o letras según se indique en pantalla.
================================================================
"""

# ============================================================
# CONSTANTES GLOBALES (alcance global - LEGB)
# ============================================================
MAX_NIVELES = 5
VIDA_INICIAL_JUGADOR = 100
DANO_BASE_JUGADOR = 20


# ============================================================
# CLASE PADRE (SUPERCLASE): Entidad
# ============================================================
class Entidad:
    """
    SUPERCLASE / CLASE PADRE: Entidad
    ---------------------------------------------------------
    Representa cualquier ser vivo del juego (jugador o enemigo).
    Contiene los atributos y métodos comunes.
    Usa encapsulamiento con atributos "protegidos" (_nombre).
    """

    def __init__(self, nombre, vida_max, dano):
        # Atributos encapsulados (convención de protegidos)
        self._nombre = nombre
        self._vida_max = vida_max
        self._vida = vida_max
        self._dano = dano
        self._vivo = True

    # ---------- Métodos de acceso (getters) ----------
    def get_nombre(self):
        return self._nombre

    def get_vida(self):
        return self._vida

    def get_vida_max(self):
        return self._vida_max

    def get_dano(self):
        return self._dano

    def esta_vivo(self):
        return self._vivo

    # ---------- Métodos comunes ----------
    def recibir_dano(self, cantidad):
        """Reduce la vida. Si llega a 0, la entidad muere."""
        if not self._vivo:
            return
        self._vida -= cantidad
        if self._vida <= 0:
            self._vida = 0
            self._vivo = False
            print(f"  >>> {self._nombre} ha sido derrotado.")

    def curar(self, cantidad):
        """Restaura vida sin superar el máximo."""
        if self._vivo:
            self._vida = min(self._vida + cantidad, self._vida_max)

    def mostrar_estado(self):
        """Muestra vida actual de forma legible."""
        barra = self._crear_barra_vida()
        print(f"  {self._nombre}: {barra} {self._vida}/{self._vida_max}")

    def _crear_barra_vida(self):
        """Método auxiliar privado para dibujar barra de vida en texto."""
        if self._vida_max == 0:
            return "[          ]"
        porcentaje = self._vida / self._vida_max
        llenos = int(porcentaje * 10)
        return "[" + "█" * llenos + "░" * (10 - llenos) + "]"

    # ---------- Métodos que serán sobrescritos (polimorfismo) ----------
    def atacar(self, objetivo):
        """
        Método base de ataque.
        Las subclases lo sobrescriben → POLIMORFISMO.
        """
        if not self._vivo or not objetivo.esta_vivo():
            return 0
        print(f"  {self._nombre} ataca a {objetivo.get_nombre()} "
              f"causando {self._dano} de daño.")
        objetivo.recibir_dano(self._dano)
        return self._dano

    def describir(self):
        """
        Método base de descripción.
        Las subclases lo sobrescriben → POLIMORFISMO.
        """
        return f"{self._nombre} (Vida: {self._vida}/{self._vida_max})"


# ============================================================
# CLASE HIJA (SUBCLASE): Jugador
# Hereda de Entidad
# ============================================================
class Jugador(Entidad):
    """
    SUBCLASE de Entidad: Jugador (Blade el Cazarecompensas)
    ---------------------------------------------------------
    Añade puntuación, nivel de espada y acciones especiales.
    """

    def __init__(self, nombre="Blade"):
        # Llamada al constructor de la superclase
        super().__init__(nombre, VIDA_INICIAL_JUGADOR, DANO_BASE_JUGADOR)
        self._puntos = 0
        self._nivel_espada = 1
        self._pociones = 2          # Pociones de curación
        self._ataques_realizados = 0

    # ---------- Getters adicionales ----------
    def get_puntos(self):
        return self._puntos

    def get_pociones(self):
        return self._pociones

    def get_nivel_espada(self):
        return self._nivel_espada

    # ---------- Métodos propios del jugador ----------
    def ganar_puntos(self, cantidad):
        self._puntos += cantidad

    def mejorar_espada(self):
        """Mejora el daño de la espada."""
        self._nivel_espada += 1
        self._dano = DANO_BASE_JUGADOR + (self._nivel_espada - 1) * 8
        print(f"\n  ¡Tu espada ha mejorado! Nivel {self._nivel_espada} "
              f"(Daño: {self._dano})")

    def usar_pocion(self):
        """Usa una poción para recuperar vida."""
        if self._pociones <= 0:
            print("  No te quedan pociones.")
            return False
        self._pociones -= 1
        curacion = 35
        self.curar(curacion)
        print(f"  Usaste una poción. Recuperaste {curacion} de vida. "
              f"(Pociones restantes: {self._pociones})")
        return True

    def atacar(self, objetivo):
        """
        POLIMORFISMO: Sobrescribe el método atacar de Entidad.
        El jugador tiene un ataque más descriptivo y puede
        fallar o hacer daño crítico de forma simple.
        """
        if not self._vivo or not objetivo.esta_vivo():
            return 0

        self._ataques_realizados += 1
        # Daño base + pequeño bonus (sin usar random)
        bonus = (self._ataques_realizados % 3) * 3
        dano_total = self._dano + bonus

        print(f"\n  ⚔️  {self._nombre} lanza un tajo con su espada "
              f"contra {objetivo.get_nombre()}!")
        print(f"     Daño infligido: {dano_total}")
        objetivo.recibir_dano(dano_total)

        if not objetivo.esta_vivo():
            puntos_ganados = 50 + (objetivo.get_vida_max() // 2)
            self.ganar_puntos(puntos_ganados)
            print(f"  +{puntos_ganados} puntos")

        return dano_total

    def describir(self):
        """POLIMORFISMO: descripción detallada del jugador."""
        return (f"{self._nombre} | Vida: {self._vida}/{self._vida_max} | "
                f"Daño: {self._dano} | Espada Nv.{self._nivel_espada} | "
                f"Puntos: {self._puntos} | Pociones: {self._pociones}")


# ============================================================
# CLASE HIJA (SUBCLASE): Enemigo
# Hereda de Entidad (clase intermedia)
# ============================================================
class Enemigo(Entidad):
    """
    SUBCLASE de Entidad: Enemigo
    ---------------------------------------------------------
    Clase intermedia. Los enemigos específicos heredan de aquí.
    """

    def __init__(self, nombre, vida_max, dano, puntos_valor, descripcion):
        super().__init__(nombre, vida_max, dano)
        self._puntos_valor = puntos_valor
        self._descripcion = descripcion

    def get_puntos_valor(self):
        return self._puntos_valor

    def atacar(self, objetivo):
        """
        POLIMORFISMO: ataque genérico de enemigo.
        """
        if not self._vivo or not objetivo.esta_vivo():
            return 0
        print(f"\n  💀 {self._nombre} ataca ferozmente a {objetivo.get_nombre()}!")
        print(f"     Daño recibido: {self._dano}")
        objetivo.recibir_dano(self._dano)
        return self._dano

    def describir(self):
        """POLIMORFISMO"""
        return f"{self._nombre} - {self._descripcion} (Vida: {self._vida}/{self._vida_max})"


# ============================================================
# SUBCLASES ESPECÍFICAS DE ENEMIGOS
# (heredan de Enemigo → herencia multinivel)
# ============================================================
class VampiroBasico(Enemigo):
    """
    SUBCLASE de Enemigo: Vampiro enemigo básico
    """

    def __init__(self):
        super().__init__(
            nombre="Vampiro",
            vida_max=45,
            dano=12,
            puntos_valor=40,
            descripcion="Un vampiro menor sediento de sangre"
        )

    def atacar(self, objetivo):
        """
        POLIMORFISMO: el vampiro básico tiene un ataque con
        posibilidad de robar un poco de vida.
        """
        dano = super().atacar(objetivo)
        # Robo de vida simple
        if self._vivo and dano > 0:
            robo = max(3, dano // 4)
            self.curar(robo)
            print(f"     El vampiro absorbe {robo} de vida.")
        return dano


class Esqueleto(Enemigo):
    """
    SUBCLASE de Enemigo: Esqueleto
    """

    def __init__(self):
        super().__init__(
            nombre="Esqueleto",
            vida_max=60,
            dano=15,
            puntos_valor=55,
            descripcion="Huesos animados que no sienten dolor"
        )

    def atacar(self, objetivo):
        """
        POLIMORFISMO: el esqueleto ataca con más fuerza pero
        es predecible.
        """
        if not self._vivo or not objetivo.esta_vivo():
            return 0
        print(f"\n  💀 El {self._nombre} golpea con su espada oxidada!")
        print(f"     Daño recibido: {self._dano}")
        objetivo.recibir_dano(self._dano)
        return self._dano


class MurcielagoGigante(Enemigo):
    """
    SUBCLASE de Enemigo: Murciélago gigante
    """

    def __init__(self):
        super().__init__(
            nombre="Murciélago Gigante",
            vida_max=35,
            dano=10,
            puntos_valor=45,
            descripcion="Criatura voladora rápida y molesta"
        )

    def atacar(self, objetivo):
        """
        POLIMORFISMO: el murciélago puede atacar dos veces
        (ráfaga).
        """
        if not self._vivo or not objetivo.esta_vivo():
            return 0
        print(f"\n  🦇 ¡El {self._nombre} se lanza en picada!")
        total = 0
        for i in range(2):
            if objetivo.esta_vivo():
                print(f"     Picotazo {i+1}: {self._dano} de daño")
                objetivo.recibir_dano(self._dano)
                total += self._dano
        return total


class Alucard(Enemigo):
    """
    SUBCLASE de Enemigo: Alucard - Jefe vampiro final
    """

    def __init__(self):
        super().__init__(
            nombre="Alucard",
            vida_max=180,
            dano=22,
            puntos_valor=300,
            descripcion="El señor de los vampiros del castillo"
        )
        self._fase = 1

    def atacar(self, objetivo):
        """
        POLIMORFISMO: Alucard cambia de comportamiento según
        su vida (fases del jefe).
        """
        if not self._vivo or not objetivo.esta_vivo():
            return 0

        # Cambio de fase
        if self._vida < self._vida_max * 0.4 and self._fase == 1:
            self._fase = 2
            self._dano = 28
            print("\n  🔥 ¡Alucard se enfurece! Su poder aumenta.")

        print(f"\n  👑 {self._nombre} desata su poder oscuro!")
        print(f"     Daño recibido: {self._dano}")
        objetivo.recibir_dano(self._dano)

        # En fase 2 tiene un ataque extra débil
        if self._fase == 2 and objetivo.esta_vivo():
            extra = 8
            print(f"     Golpe adicional de sombra: {extra} de daño")
            objetivo.recibir_dano(extra)
            return self._dano + extra
        return self._dano

    def describir(self):
        """POLIMORFISMO: descripción especial del jefe."""
        fase_txt = " (¡ENFURECIDO!)" if self._fase == 2 else ""
        return (f"👑 {self._nombre}{fase_txt} - {self._descripcion} "
                f"(Vida: {self._vida}/{self._vida_max})")


# ============================================================
# FUNCIONES AUXILIARES DEL JUEGO
# ============================================================
def limpiar_pantalla():
    """Simula limpiar la consola imprimiendo líneas en blanco."""
    print("\n" * 3)


def pausa():
    """Espera a que el usuario presione Enter."""
    input("\n  Pulsa ENTER para continuar...")


def mostrar_titulo():
    """Muestra el título del juego de forma estética."""
    print("=" * 60)
    print("                    B L A D E")
    print("              Cazarecompensas del Castillo")
    print("=" * 60)


def mostrar_bienvenida():
    """Mensaje de bienvenida al iniciar el programa."""
    mostrar_titulo()
    print("""
  Un cazarecompensas es contratado para investigar un castillo
  en medio de la nada y averiguar qué hay dentro...

  Pero es engañado: el castillo está lleno de vampiros.
  Es casi imposible sobrevivir. Solo depende de su espada
  y de sus habilidades.

  ¿Lograrás escapar con vida?
    """)
    pausa()


def pedir_opcion(mensaje, opciones_validas):
    """
    Solicita una opción al usuario con manejo de errores.
    opciones_validas: lista o tupla de strings aceptados.
    """
    while True:
        try:
            eleccion = input(mensaje).strip().lower()
            if eleccion in opciones_validas:
                return eleccion
            print(f"  Opción no válida. Elige entre: {', '.join(opciones_validas)}")
        except (EOFError, KeyboardInterrupt):
            print("\n  Entrada interrumpida. Intentando de nuevo...")
        except Exception as e:
            print(f"  Error inesperado: {e}. Intenta otra vez.")


# ============================================================
# SISTEMA DE COMBATE (turno a turno)
# ============================================================
def combate(jugador, enemigo):
    """
    Gestiona un combate completo entre el jugador y un enemigo.
    Retorna True si el jugador gana, False si pierde.
    """
    print("\n" + "-" * 50)
    print(f"  ¡COMBATE!  {jugador.get_nombre()} vs {enemigo.get_nombre()}")
    print("-" * 50)
    print(f"  {enemigo.describir()}")
    pausa()

    turno = 1
    while jugador.esta_vivo() and enemigo.esta_vivo():
        print(f"\n  ===== TURNO {turno} =====")
        jugador.mostrar_estado()
        enemigo.mostrar_estado()

        # Menú de acciones del jugador
        print("\n  ¿Qué deseas hacer?")
        print("  1. Atacar")
        print("  2. Usar poción")
        print("  3. Intentar huir (solo a veces funciona)")

        opcion = pedir_opcion("  Elige (1/2/3): ", ("1", "2", "3"))

        if opcion == "1":
            jugador.atacar(enemigo)
        elif opcion == "2":
            if not jugador.usar_pocion():
                continue          # No pierde el turno si no tenía pociones
        elif opcion == "3":
            # Huida simple sin random: se basa en turnos
            if turno % 3 == 0:
                print("  ¡Lograste escapar del combate!")
                return True
            else:
                print("  ¡No pudiste escapar!")

        # Si el enemigo sigue vivo, ataca
        if enemigo.esta_vivo() and jugador.esta_vivo():
            enemigo.atacar(jugador)

        turno += 1

    if jugador.esta_vivo():
        print(f"\n  ★ ¡Has derrotado a {enemigo.get_nombre()}!")
        return True
    else:
        print(f"\n  ✖ Has sido derrotado por {enemigo.get_nombre()}...")
        return False


# ============================================================
# GENERACIÓN DE NIVELES
# ============================================================
def crear_enemigos_nivel(numero_nivel):
    """
    Devuelve una lista de enemigos según el nivel.
    Usa herencia y polimorfismo: todos son tratados como Enemigo.
    """
    if numero_nivel == 1:
        return [VampiroBasico(), VampiroBasico()]
    elif numero_nivel == 2:
        return [VampiroBasico(), Esqueleto(), VampiroBasico()]
    elif numero_nivel == 3:
        return [Esqueleto(), MurcielagoGigante(), Esqueleto(), MurcielagoGigante()]
    elif numero_nivel == 4:
        return [VampiroBasico(), Esqueleto(), MurcielagoGigante(),
                MurcielagoGigante(), Esqueleto()]
    else:  # Nivel 5 - Jefe
        return [VampiroBasico(), MurcielagoGigante(), Alucard()]


def jugar_nivel(jugador, numero_nivel):
    """
    Ejecuta un nivel completo.
    Retorna True si el jugador completa el nivel, False si muere.
    """
    limpiar_pantalla()
    print("=" * 60)
    print(f"                 NIVEL {numero_nivel} / {MAX_NIVELES}")
    print("=" * 60)

    if numero_nivel == 5:
        print("\n  Has llegado a la sala del trono...")
        print("  El aire se vuelve pesado. Alucard te espera.")
    else:
        print(f"\n  Avanzas por los pasillos del castillo...")
        print(f"  Se escuchan ruidos en la oscuridad.")

    enemigos = crear_enemigos_nivel(numero_nivel)
    print(f"\n  Enemigos en este nivel: {len(enemigos)}")
    for e in enemigos:
        print(f"   • {e.describir()}")

    pausa()

    # Combatir uno a uno
    for i, enemigo in enumerate(enemigos, 1):
        if not jugador.esta_vivo():
            return False
        print(f"\n  --- Enemigo {i} de {len(enemigos)} ---")
        gano = combate(jugador, enemigo)
        if not gano:
            return False
        # Pequeña recompensa entre combates
        if jugador.esta_vivo() and i < len(enemigos):
            print("\n  Encuentras un momento para recuperar el aliento...")
            jugador.curar(10)
            print("  (+10 de vida)")

    # Recompensa de nivel
    if jugador.esta_vivo():
        print(f"\n  ★ ¡Nivel {numero_nivel} completado!")
        jugador.ganar_puntos(100 * numero_nivel)
        if numero_nivel % 2 == 0:
            jugador.mejorar_espada()
        if numero_nivel == 3:
            jugador._pociones += 1
            print("  Encontraste una poción extra.")
        pausa()
        return True
    return False


# ============================================================
# MENÚS DEL JUEGO
# ============================================================
def menu_principal():
    """Muestra el menú principal y retorna la opción elegida."""
    limpiar_pantalla()
    mostrar_titulo()
    print("""
  1. JUGAR
  2. CONFIGURACIÓN
  3. CRÉDITOS
  4. SALIR
    """)
    return pedir_opcion("  Elige una opción (1-4): ", ("1", "2", "3", "4"))


def mostrar_configuracion(dificultad_actual):
    """Pantalla de configuración (simple)."""
    limpiar_pantalla()
    print("=" * 60)
    print("                   CONFIGURACIÓN")
    print("=" * 60)
    print(f"\n  Dificultad actual: {dificultad_actual}")
    print("""
  1. Fácil   (más vida y daño)
  2. Normal  (valores por defecto)
  3. Difícil (menos vida)
  4. Volver al menú
    """)
    return pedir_opcion("  Elige (1-4): ", ("1", "2", "3", "4"))


def mostrar_creditos():
    """Pantalla de créditos."""
    limpiar_pantalla()
    print("=" * 60)
    print("                     CRÉDITOS")
    print("=" * 60)
    print("""
  BLADE - Videojuego de consola

  Historia:
  Un cazarecompensas contratado para investigar un castillo
  que resulta estar lleno de vampiros.

  Personajes:
  1. Cazarecompensas Blade (jugador)
  2. Vampiro enemigo básico
  3. Esqueletos
  4. Murciélago gigante
  5. Alucard - Jefe vampiro final

  Tecnologías usadas:
  • Python puro (sin librerías externas)
  • Clases, herencia y polimorfismo
  • Encapsulamiento
  • Funciones, listas, tuplas
  • Manejo de errores (try-except)

  Proyecto académico - Todos los derechos del diseño
  pertenecen al estudiante.
    """)
    pausa()


def aplicar_dificultad(jugador, dificultad):
    """Ajusta las estadísticas del jugador según la dificultad."""
    if dificultad == "Fácil":
        jugador._vida_max = 140
        jugador._vida = 140
        jugador._dano = 28
        jugador._pociones = 3
    elif dificultad == "Difícil":
        jugador._vida_max = 75
        jugador._vida = 75
        jugador._dano = 16
        jugador._pociones = 1
    # Normal usa los valores por defecto del constructor


def bucle_juego(dificultad):
    """
    Bucle principal de la partida.
    Crea al jugador y recorre los 5 niveles.
    """
    jugador = Jugador("Blade")
    aplicar_dificultad(jugador, dificultad)

    print("\n  Tu aventura comienza...")
    print(f"  {jugador.describir()}")
    pausa()

    for nivel in range(1, MAX_NIVELES + 1):
        if not jugador.esta_vivo():
            break
        exito = jugar_nivel(jugador, nivel)
        if not exito:
            break

    # Resultado final
    limpiar_pantalla()
    if jugador.esta_vivo() and nivel == MAX_NIVELES:
        print("=" * 60)
        print("                    ¡VICTORIA!")
        print("=" * 60)
        print("""
  Blade ha derrotado a Alucard y ha escapado del castillo.
  Los rayos del sol brillan sobre ti por primera vez en días.

  ¡Has sobrevivido a la pesadilla!
        """)
    else:
        print("=" * 60)
        print("                    GAME OVER")
        print("=" * 60)
        print("""
  Las criaturas del castillo han sido demasiado fuertes.
  Blade cae en la oscuridad...
        """)

    print(f"\n  Puntuación final: {jugador.get_puntos()}")
    print(f"  Nivel alcanzado: {nivel}/{MAX_NIVELES}")
    print(f"  Estado final: {jugador.describir()}")
    pausa()


# ============================================================
# FUNCIÓN PRINCIPAL (punto de entrada)
# ============================================================
def main():
    """
    Función principal del programa.
    Controla el flujo del menú y el inicio del juego.
    """
    # Mensaje de bienvenida (Etapa 1)
    mostrar_bienvenida()

    dificultad = "Normal"

    # Bucle del menú principal
    while True:
        opcion = menu_principal()

        if opcion == "1":          # JUGAR
            bucle_juego(dificultad)
        elif opcion == "2":        # CONFIGURACIÓN
            while True:
                eleccion = mostrar_configuracion(dificultad)
                if eleccion == "1":
                    dificultad = "Fácil"
                    print("\n  Dificultad cambiada a: Fácil")
                    pausa()
                elif eleccion == "2":
                    dificultad = "Normal"
                    print("\n  Dificultad cambiada a: Normal")
                    pausa()
                elif eleccion == "3":
                    dificultad = "Difícil"
                    print("\n  Dificultad cambiada a: Difícil")
                    pausa()
                elif eleccion == "4":
                    break
        elif opcion == "3":        # CRÉDITOS
            mostrar_creditos()
        elif opcion == "4":        # SALIR
            print("\n  Gracias por jugar BLADE. ¡Hasta la próxima!")
            print("  Cerrando el programa...\n")
            break


# ============================================================
# PUNTO DE ENTRADA DEL PROGRAMA
# ============================================================
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Programa interrumpido por el usuario. ¡Adiós!")
    except Exception as error:
        print(f"\n  Error inesperado: {error}")
        print("  El programa se cerrará.")