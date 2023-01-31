﻿using System.Drawing;

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
            new Question {
                QuizQuestion = "In which of the following films did {0} appear?",
                Query = "SELECT DISTINCT ?filmTitle WHERE " +
                    "{ ?card foaf:member gada:univ_Star_Wars; rdfs:label @value; swapi:film ?film. ?film rdfs:label ?filmTitle.}",
                QuestionType = Universe.StarWars,
                MultipleChoice = true,
                SparqlEndpointType = SparqlEndPoint.TripleStore
            },
            new Question {
                QuizQuestion = "What is {0}'s birthplace?",
                Query = "SELECT (GROUP_CONCAT(DISTINCT ?birthPlaceName; separator=\", \") as ?fullBirthPlace) " +
                "WHERE { ?card foaf:member gada:univ_Star_Trek; sdo:birthPlace ?birthPlace; rdfs:label @value. " +
                        "?birthPlace rdfs:label ?birthPlaceName.} GROUP BY ?card",
                QuestionType = Universe.StarTrek,
                MultipleChoice = false,
                SparqlEndpointType = SparqlEndPoint.TripleStore
            }
        };
    }
}
