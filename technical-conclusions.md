# Proceso, Conclusiones y Mejoras 🎯

## Detalles técnicos y decisiones

- Especifico la estructura del JSON aunque con structured outputs quizás no haría falta. Aun así, creo que refuerza la salida y nos deja los prompts preparados para modelos que no tengan structured output.

- No he metido retries si falla la estructura porque confío en que structured output nos dará una buena salida. Pero estaría bien que si falla, reintente - o incluso tener un prompt "arregla-JSONs" para estos casos.

- He puesto las variables con explicaciones (tipo `relevance_explanation`) antes que las conclusiones finales (`relevance`) para ayudar al Chain of Thought y sacar mejor resultado. Se podría ir a un modelo má CoT pidiendo en una variable los `steps` de razonamiento antes del resultado.

- Uso temperatura baja para que el resultado sea más predecible.

- También uso seed para que las llamadas den mismo resultado... aunque curiosamente a veces me sale una puntuación distinta en habilidades. No he conseguido pillar por qué - habría que investigarlo más.

## Lo que podríamos mejorar

### Sobre la puntuación y evaluación

- La verdad es que la puntuación que estamos sacando no termina de ser del todo relevante para las habilidades. Habría que darle una vuelta al sistema - ¿y si incluimos un prompt juez que evalúe todo el contexto del CV y los resultados para ver si están bien ajustados o se pueden mejorar?

### Validación de datos

- Estaría bien meter algún prompt extra para verificar que estamos extrayendo bien la experiencia, habilidades y educación. Según el formato del CV nos puede estar dando valores incorrectos en algunos campos (fechas mal parseadas, nombres de empresa confundidos...).

## Sobre los prompts y el razonamiento

- Con el `experience_prompt` ya conseguimos la funcionalidad principal que nos piden. A este le mandamos el CV entero y listo.

- El `summary_prompt` nos da la conclusión final juntando los resultados de la evaluación + la parte numérica calculada en código.

- Los otros prompts (`experience_result.json` y `skills_result.json`) no son imprescindibles para la prueba, pero nos dan una evaluación más completa.

- Como estamos usando IA generativa, he preferido pedir evaluaciones cualitativas y luego mapearlas a números en el código - los valores numéricos directos pueden ser demasiado aleatorios.

- He usado español en el prompt para que el modelo responda en este idioma. Podríamos reforzarlo especificando el idioma de respuesta explícitamente. Lo probé con mi CV en inglés y me contestó algunas cosas en inglés, así que ahí sí que necesitaríamos el refuerzo.
