using System.Drawing;

namespace QuizAPI.Core
{
    public class Quiz
    {
        public List<Question> Questions = new List<Question> {
            new Question
            {
                 QuizQuestion = "From which universe is {0}?",
                 Query = "SELECT ?universeName WHERE {?subject foaf:member ?universe; rdfs:label @value. ?universe rdfs:label ?universeName }",
                 MultipleChoice = false,
                 SparqlEndpointType = SparqlEndPoint.TripleStore
            },
            new Question {
                QuizQuestion = "What colour is {0}?",
                Query = "SELECT ?colour " +
                        "WHERE {?pokemon foaf:member gada:univ_Pokemon; rdfs:label @value; poke:colour ?colour.} LIMIT 10",
                QuestionType = Universe.Pokemon,
                MultipleChoice = false,
                SparqlEndpointType = SparqlEndPoint.TripleStore
            },
            new Question
            {
                QuizQuestion = "Which of the following abilities does {0} have? ",
                Query = "SELECT ?ability WHERE { ?pokemon foaf:member gada:univ_Pokemon; rdfs:label @value; poke:ability ?ability;}",
                QuestionType = Universe.Pokemon,
                MultipleChoice = true,
                SparqlEndpointType = SparqlEndPoint.TripleStore
            },
            new Question
            {
                QuizQuestion = "Which of the following alliances does {0} belong to?",
                Query = "SELECT (STR(?allianceName) as ?alliances) WHERE " +
                        "{ ?character a dbo:ComicsCharacter; rdfs:label @value@en; dbp:alliances ?alliance. " +
                        "?alliance rdfs:label ?allianceName. FILTER(LANG(?allianceName)=\"en\") } LIMIT 10",
                QuestionType= Universe.Marvel,
                MultipleChoice =  true,
                SparqlEndpointType = SparqlEndPoint.DBPedia
            },
            new Question {
                QuizQuestion = "Which of the following occupations does {0} have?",
                Query = "SELECT ?ocupation " +
                        "WHERE { ?hero foaf:member gada:univ_Marvel; rdfs:label @value; sdo:hasOccupation ?ocupation. }",
                QuestionType = Universe.Marvel,
                MultipleChoice = true,
                SparqlEndpointType = SparqlEndPoint.TripleStore
            },
            new Question
            {
                QuizQuestion = "In which comic does {0} debut?",
                Query = "SELECT (STR(?comicBook) AS ?debut) WHERE {{?character a dbo:FictionalCharacter; rdfs:label @value@en; dbp:debut ?comicBook.} UNION { ?character a dbo:FictionalCharacter; dbp:characterName @value@en; dbp:debut ?comicBook.} OPTIONAL {FILTER(LANG(?comicBook)=\"en\").} } LIMIT 1",
                QuestionType = Universe.Marvel,
                MultipleChoice = false,
                SparqlEndpointType = SparqlEndPoint.DBPedia
            },
            new Question {
                QuizQuestion = "In which of the following films did {0} appear?",
                Query = "SELECT DISTINCT ?filmTitle WHERE " +
                    "{ ?card foaf:member gada:univ_Star_Wars; rdfs:label @value; swapi:film ?film. ?film rdfs:label ?filmTitle.}",
                QuestionType = Universe.StarWars,
                MultipleChoice = true,
                SparqlEndpointType = SparqlEndPoint.TripleStore
            },
            new Question
            {
                QuizQuestion = "Which of the following characters are related to {0}?",
                Query = "SELECT (STR(?relativeName) as ?relatives) WHERE { ?character a dbo:FictionalCharacter; rdfs:label @value@en; dbo:relative ?relative. ?relative a dbo:FictionalCharacter; rdfs:label ?relativeName. FILTER(LANG(?relativeName)=\"en\")}",
                QuestionType = Universe.StarWars,
                MultipleChoice = true,
                SparqlEndpointType = SparqlEndPoint.DBPedia
            },
            new Question {
                QuizQuestion = "What is {0}'s birthplace?",
                Query = "SELECT (GROUP_CONCAT(DISTINCT ?birthPlaceName; separator=\", \") as ?fullBirthPlace) " +
                "WHERE { ?card foaf:member gada:univ_Star_Trek; sdo:birthPlace ?birthPlace; rdfs:label @value. " +
                        "?birthPlace rdfs:label ?birthPlaceName.} GROUP BY ?card",
                QuestionType = Universe.StarTrek,
                MultipleChoice = false,
                SparqlEndpointType = SparqlEndPoint.TripleStore
            }, 
            new Question
            {
                QuizQuestion = "Which of the following characteristics are specific to {0}?",
                Query = "SELECT (STR(?speciesName) AS ?type) WHERE{?character foaf:member gada:univ_Star_Trek;rdfs:label @value;" +
                            "ssn:hasProperty ?species.?species owl:sameAs ?resource. " +
                            "SERVICE<https://dbpedia.org/sparql/> {?resource rdfs:label ?speciesName.FILTER(LANG(?speciesName)=\"en\")}}",
                QuestionType = Universe.StarTrek,
                MultipleChoice = true,
                SparqlEndpointType = SparqlEndPoint.TripleStore
            }
        };
    }
}
