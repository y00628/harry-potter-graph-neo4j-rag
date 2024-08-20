// Load Session Data from JSON
WITH './data/en_train_set.json' AS url
CALL apoc.load.json(url) YIELD value AS sessionData

// Create a Chapter node
MERGE (chapter:Chapter {position: sessionData["Session-1"].position})
SET chapter.name = sessionData["Session-1"].position

// Create Speaker nodes and relationships to Chapter
FOREACH (speaker IN sessionData["Session-1"].speakers |
    MERGE (s:Speaker {name: speaker})
    MERGE (s)-[:PARTICIPATES_IN]->(chapter)
)

// Create Scene nodes and relationships to Chapter
WITH sessionData, chapter
UNWIND sessionData["Session-1"].scene AS sceneLine
MERGE (scene:Scene {text: sceneLine})
MERGE (scene)-[:PART_OF]->(chapter)
