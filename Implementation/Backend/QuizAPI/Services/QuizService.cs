using QuizAPI.Core;
using VDS.RDF.Query;
using VDS.RDF.Parsing;

namespace QuizAPI.Services
{
    public class QuizService : IQuizService
    {
        private readonly Quiz quiz;
        static Random random = new Random();

        public QuizService(Quiz quiz)
        {
            this.quiz = quiz;
        }

        public List<string> GetQueryAnswer(string querry, string character)
        {
            List<string> resultsList = new List<string>();  

            SparqlParameterizedString queryString = new SparqlParameterizedString();

            queryString.Namespaces.AddNamespace("foaf", new Uri("http://xmlns.com/foaf/0.1/"));
            queryString.Namespaces.AddNamespace("gada", new Uri("https://gada.cards.game.namespace.com/"));
            queryString.Namespaces.AddNamespace("poke", new Uri("https://triplydb.com/academy/pokemon/vocab/"));
            queryString.Namespaces.AddNamespace("rdfs", new Uri("http://www.w3.org/2000/01/rdf-schema#"));

            queryString.Namespaces.AddNamespace("dbo", new Uri("http://dbpedia.org/ontology/"));
            queryString.Namespaces.AddNamespace("geo", new Uri("http://www.opengis.net/ont/geosparql#"));
            queryString.Namespaces.AddNamespace("owl", new Uri("http://www.w3.org/2002/07/owl#"));
            queryString.Namespaces.AddNamespace("sdo", new Uri("https://schema.org/"));
            queryString.Namespaces.AddNamespace("ssn", new Uri("http://www.w3.org/ns/ssn/"));
            queryString.Namespaces.AddNamespace("swapi", new Uri("https://swapi.co/vocabulary/"));
            queryString.Namespaces.AddNamespace("xsd", new Uri("http://www.w3.org/2001/XMLSchema#"));
            queryString.Namespaces.AddNamespace("po", new Uri("http://purl.org/ontology/po/"));


            queryString.CommandText = querry;
            queryString.SetLiteral("value", character);

            SparqlQueryParser parser = new SparqlQueryParser();
            SparqlQuery query = parser.ParseFromString(queryString);

            SparqlRemoteEndpoint endpoint = new SparqlRemoteEndpoint(new Uri("http://localhost:3030/gada_set2/query"));
            SparqlResultSet results = endpoint.QueryWithResultSet(query.ToString());
          
            
            //WHEN ONLY A COLUMN IS RETURNED
            foreach (SparqlResult result in results)
            {
                resultsList.Add(result[0].ToString());
                Console.WriteLine(result.ToString());
            }
            return resultsList;
        }

        public string GetQueryOfQuestion(string question)
        {
            return quiz.Questions.Find(q => q.QuizQuestion.Equals(question)).Query;
        }

        private string GetCharacterUniverse(string characterName)
        {
            SparqlParameterizedString queryString = new SparqlParameterizedString();
            queryString.Namespaces.AddNamespace("foaf", new Uri("http://xmlns.com/foaf/0.1/"));
            queryString.Namespaces.AddNamespace("rdfs", new Uri("http://www.w3.org/2000/01/rdf-schema#"));

            queryString.CommandText = "SELECT ?universeName WHERE {  " +
                "?character foaf:member ?universe;  rdfs:label @value. ?universe rdfs:label ?universeName.}";
            queryString.SetLiteral("value", characterName);

            SparqlQueryParser parser = new SparqlQueryParser();
            SparqlQuery query = parser.ParseFromString(queryString);

            SparqlRemoteEndpoint endpoint = new SparqlRemoteEndpoint(new Uri("http://localhost:3030/gada_set2/query"));
            SparqlResultSet results = endpoint.QueryWithResultSet(query.ToString());

            var result = results.First().ToString();
            var universe = result.Substring(result.IndexOf("=") + 1).Trim();

            return universe;
        }

        public QuestionToReturn GetRandomQuestion(List<string> characters)
        {
            int index;
            int optionIndex = 1;
            var queryAnswer = new List<string>();

            var selectedCharacter = GetRandomCharacter(characters);

            var characterUniverse = GetCharacterUniverse(selectedCharacter);

            var questions = quiz.Questions.Where(q => q.QuestionType.ToLower().Equals(characterUniverse.ToLower())).ToList();

            index = random.Next(questions.Count);
            Question question = questions[index];
            var quizQuestion = String.Format(question.QuizQuestion, selectedCharacter);

            QuestionToReturn questionToReturn = new QuestionToReturn();
            questionToReturn.Question = quizQuestion;
            questionToReturn.QuestionType = characterUniverse;
            questionToReturn.Subject = selectedCharacter;

            var characterList = GetCharacters(characterUniverse);

            queryAnswer = GetQueryAnswer(question.Query, selectedCharacter);
            while (queryAnswer.Count == 0)
            {
                selectedCharacter = GetRandomCharacter(characters.Where(c => characterList.Contains(c)).ToList());
                queryAnswer = GetQueryAnswer(question.Query, selectedCharacter);
                questionToReturn.Subject = selectedCharacter;
            }

            questionToReturn.Options = new Dictionary<string, List<string>>();

            if (!question.MultipleChoice)
            {
                questionToReturn.Options.Add("option" + (optionIndex++).ToString(), queryAnswer);

                var character = GetRandomCharacter(characterList);
                characterList.Remove(character);
                queryAnswer = GetQueryAnswer(question.Query, character);
                while (queryAnswer.Count == 0)
                {
                    character = GetRandomCharacter(characterList);
                    queryAnswer = GetQueryAnswer(question.Query, character);
                    characterList.Remove(character);
                }
                questionToReturn.Options.Add("option" + (optionIndex++).ToString(), queryAnswer);

                character = GetRandomCharacter(characterList);
                queryAnswer = GetQueryAnswer(question.Query, character);
                while (queryAnswer.Count == 0)
                {
                    character = GetRandomCharacter(characterList);
                    queryAnswer = GetQueryAnswer(question.Query, character);
                    characterList.Remove(character);
                }
                questionToReturn.Options.Add("option" + optionIndex.ToString(), queryAnswer);
            }
            else
            {
                var count = queryAnswer.Count;
                string character;

                index = random.Next(queryAnswer.Count);
                var option = queryAnswer[index];
                questionToReturn.Options.Add("option" + (optionIndex++).ToString(), new List<string> { option });
                queryAnswer.Remove(option);

                if (count >= 2)
                {
                    index = random.Next(queryAnswer.Count);
                    option = queryAnswer[index];
                    questionToReturn.Options.Add("option" + (optionIndex++).ToString(), new List<string> { option });
                }
                else
                {   
                    character = GetRandomCharacter(characterList);
                    queryAnswer = GetQueryAnswer(question.Query, character);
                    while (queryAnswer.Count == 0)
                    {
                        character = GetRandomCharacter(characterList);
                        queryAnswer = GetQueryAnswer(question.Query, character);
                        characterList.Remove(character);
                    }
                    index = random.Next(queryAnswer.Count);
                    option = queryAnswer[index];
                    questionToReturn.Options.Add("option" + (optionIndex++).ToString(), new List<string> { option });
                    characterList.Remove(character);
                }
                character = GetRandomCharacter(characterList);
                queryAnswer = GetQueryAnswer(question.Query, character);
                while(queryAnswer.Count == 0)
                {
                    character = GetRandomCharacter(characterList);
                    queryAnswer = GetQueryAnswer(question.Query, character);
                    characterList.Remove(character);
                }
                index = random.Next(queryAnswer.Count);
                option = queryAnswer[index];
                questionToReturn.Options.Add("option" + (optionIndex++).ToString(), new List<string> { option });
            }

            return questionToReturn;
        }

        private string GetRandomCharacter(List<string> characterList)
        {
            int index = random.Next(characterList.Count);
            var character = characterList[index];

            return character;
        }

        private List<String> GetCharacters(string universe)
        {

            var characterList = new List<string>(); 

            SparqlParameterizedString queryString = new SparqlParameterizedString();

            queryString.Namespaces.AddNamespace("foaf", new Uri("http://xmlns.com/foaf/0.1/"));
            queryString.Namespaces.AddNamespace("rdfs", new Uri("http://www.w3.org/2000/01/rdf-schema#"));

            queryString.CommandText = "SELECT ?characterName " +
                "WHERE { ?pokemon foaf:member ?universe; rdfs:label ?characterName. ?universe rdfs:label @value.}";
            queryString.SetLiteral("value", universe);

            SparqlQueryParser parser = new SparqlQueryParser();
            SparqlQuery query = parser.ParseFromString(queryString);

            SparqlRemoteEndpoint endpoint = new SparqlRemoteEndpoint(new Uri("http://localhost:3030/gada_set2/query"));
            SparqlResultSet results = endpoint.QueryWithResultSet(query.ToString());

            characterList = results.Select(x => x[0].ToString()).ToList();  

            return characterList;
        }


        //FOR NOW, for questions with only one answer option
        public bool CheckAnswer(Answer answer)
        {
            string questionTemplate="";
            string questionAnswer = answer.QuestionAnswer.First();

            var allQuestionsTemplates = quiz.Questions.Select(x => x.QuizQuestion).ToList();

            foreach (var template in allQuestionsTemplates)
            {
                var formattedQuestion = string.Format(template, answer.Subject);
                if (formattedQuestion.ToLower().Equals(answer.Question.ToLower()))
                {
                    questionTemplate = template;
                    break;
                }
            }
            if (!string.IsNullOrEmpty(questionTemplate))
            {
                var query = GetQueryOfQuestion(questionTemplate);

                var queryResult = GetQueryAnswer(query, answer.Subject).FirstOrDefault();

                if (questionAnswer.Equals(queryResult))
                    return true;
            }

            return false;
        }

    }
}
