namespace QuizAPI.Core
{
    public class Quiz
    {
        public List<Question> Questions = new List<Question> {
            new Question {
                QuizQuestion = "What colour is {0}?",
                Query = "SELECT ?colour " +
                        "WHERE {?pokemon foaf:member gada:univ_Pokemon; rdfs:label @value; poke:colour ?colour.} LIMIT 10",
                QuestionType = Universe.Pokemon
            },
            new Question {
                QuizQuestion = "A MARVEL question",
                Query = "Query for marvel",
                QuestionType = Universe.Marvel
            },
            new Question {
                QuizQuestion = "A STAR-WARS question",
                Query = "Query for STAR-WARS",
                QuestionType = Universe.StarWars
            },
            new Question {
                QuizQuestion = "A STAR-TREK question",
                Query = "Query for STAR-TREK",
                QuestionType = Universe.StarTrek
            }
        };
    }
}
