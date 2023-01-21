namespace QuizAPI.Core
{
    public class Quiz
    {
        public List<Question> Questions = new List<Question> {
            new Question {
                QuizQuestion = "What colour is {0}?",
                Query = "SELECT ?colour " +
                        "WHERE {?pokemon foaf:member gada:univ_Pokemon; rdfs:label @value; poke:colour ?colour.} LIMIT 10",
                QuestionType = Universe.Pokemon,
                MultipleChoice = false
            },
            new Question {
                QuizQuestion = "Which of the following occupations does {0} have?",
                Query = "SELECT ?ocupation " +
                        "WHERE { ?hero foaf:member gada:univ_Marvel; rdfs:label @value; sdo:hasOccupation ?ocupation. }",
                QuestionType = Universe.Marvel,
                MultipleChoice = true
            },
            new Question {
                QuizQuestion = "In which of the following films did {0} appear?",
                Query = "SELECT DISTINCT ?filmTitle WHERE " +
                    "{ ?card foaf:member gada:univ_Star_Wars; rdfs:label @value; swapi:film ?film. ?film rdfs:label ?filmTitle.}",
                QuestionType = Universe.StarWars,
                MultipleChoice = true
            },
            new Question {
                QuizQuestion = "What is {0}'s birthplace?",
                Query = "SELECT (GROUP_CONCAT(DISTINCT ?birthPlaceName; separator=\", \") as ?fullBirthPlace) " +
                "WHERE { ?card foaf:member gada:univ_Star_Trek; sdo:birthPlace ?birthPlace; rdfs:label @value. " +
                        "?birthPlace rdfs:label ?birthPlaceName.} GROUP BY ?card",
                QuestionType = Universe.StarTrek,
                MultipleChoice = false
            }
        };
    }
}
