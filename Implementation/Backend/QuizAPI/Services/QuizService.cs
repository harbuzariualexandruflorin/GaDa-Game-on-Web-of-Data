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

            var question = quiz.Questions.FirstOrDefault(q => q.Query.Equals(querry));

            SparqlParameterizedString queryString = new SparqlParameterizedString();

            queryString.Namespaces.AddNamespace("foaf", new Uri("http://xmlns.com/foaf/0.1/"));
            queryString.Namespaces.AddNamespace("gada", new Uri("https://gada.cards.game.namespace.com/"));
            queryString.Namespaces.AddNamespace("poke", new Uri("https://triplydb.com/academy/pokemon/vocab/"));
            queryString.Namespaces.AddNamespace("rdfs", new Uri("http://www.w3.org/2000/01/rdf-schema#"));
            queryString.Namespaces.AddNamespace("db", new Uri("http://dbpedia.org/"));
            queryString.Namespaces.AddNamespace("dbp", new Uri("http://dbpedia.org/property/"));
            queryString.Namespaces.AddNamespace("dbr", new Uri("http://dbpedia.org/resource/"));
            //queryString.Namespaces.AddNamespace("dbc", new Uri("http://dbpedia.org/resource/Category:"));
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

            SparqlRemoteEndpoint endpoint = new SparqlRemoteEndpoint(new Uri(question.SparqlEndpointType));
            SparqlResultSet results = endpoint.QueryWithResultSet(query.ToString());
            
            foreach (SparqlResult result in results)
            {
                Console.WriteLine(result.ToString());
                resultsList.Add(result[0].ToString());
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

            SparqlRemoteEndpoint endpoint = new SparqlRemoteEndpoint(new Uri("http://localhost:3030/gada_set/query"));
            SparqlResultSet results = endpoint.QueryWithResultSet(query.ToString());

            var result = results.First().ToString();
            var universe = result.Substring(result.IndexOf("=") + 1).Trim();

            return universe;
        }

        public QuestionToReturn GetRandomQuestion(string characterName)
        {
            int index;
            int optionIndex = 1;
            var queryAnswer = new List<string>();

            //var selectedCharacter = GetRandomCharacter(characters);
            var selectedCharacter = characterName;

            var characterUniverse = GetCharacterUniverse(selectedCharacter);

            var questions = quiz.Questions.Where(q => q.QuestionType.ToLower().Equals(characterUniverse.ToLower())).ToList();

            index = random.Next(questions.Count);
            Question question = questions[index];
            var quizQuestion = String.Format(question.QuizQuestion, selectedCharacter);

            QuestionToReturn questionToReturn = new QuestionToReturn();
            questionToReturn.Question = quizQuestion;
            //questionToReturn.QuestionType = characterUniverse;
            questionToReturn.Subject = selectedCharacter;
            questionToReturn.Avatar = GetCharacterAvatar(selectedCharacter, characterUniverse);

            var characterList = GetCharacters(characterUniverse);

            queryAnswer = GetQueryAnswer(question.Query, selectedCharacter);
            //while (queryAnswer.Count == 0)
            //{
            //    selectedCharacter = GetRandomCharacter(characters.Where(c => characterList.Contains(c)).ToList());
            //    queryAnswer = GetQueryAnswer(question.Query, selectedCharacter);
            //    questionToReturn.Subject = selectedCharacter;
            //    questionToReturn.Avatar = GetCharacterAvatar(selectedCharacter, GetCharacterUniverse(selectedCharacter));
            //}

            questionToReturn.Options = new Dictionary<string, string>();

            if (!question.MultipleChoice)
            {
                questionToReturn.Options.Add("option" + (optionIndex++).ToString(), queryAnswer[0]);

                var character = GetRandomCharacter(characterList);
                characterList.Remove(character);
                queryAnswer = GetQueryAnswer(question.Query, character);

                if (queryAnswer.Count > 0 && questionToReturn.Options.Values.Contains(queryAnswer[0])) //*
                    queryAnswer.Remove(queryAnswer[0]);

                while (queryAnswer.Count == 0)
                {
                    character = GetRandomCharacter(characterList);
                    queryAnswer = GetQueryAnswer(question.Query, character);
                    if (queryAnswer.Count > 0 && questionToReturn.Options.Values.Contains(queryAnswer[0])) //*
                        queryAnswer.Remove(queryAnswer[0]);
                    characterList.Remove(character);
                }
                questionToReturn.Options.Add("option" + (optionIndex++).ToString(), queryAnswer[0]);

                character = GetRandomCharacter(characterList);
                queryAnswer = GetQueryAnswer(question.Query, character);
                if (queryAnswer.Count > 0 && questionToReturn.Options.Values.Contains(queryAnswer[0])) //*
                    queryAnswer.Remove(queryAnswer[0]);

                while (queryAnswer.Count == 0)
                {
                    character = GetRandomCharacter(characterList);
                    queryAnswer = GetQueryAnswer(question.Query, character);
                    if (queryAnswer.Count > 0 && questionToReturn.Options.Values.Contains(queryAnswer[0])) //*
                        queryAnswer.Remove(queryAnswer[0]);
                    characterList.Remove(character);
                }
                questionToReturn.Options.Add("option" + optionIndex.ToString(), queryAnswer[0]);
            }
            else
            {
                var count = queryAnswer.Count;
                string character;

                index = random.Next(queryAnswer.Count);
                var option = queryAnswer[index];
                questionToReturn.Options.Add("option" + (optionIndex++).ToString(), option );
                queryAnswer.Remove(option);

                if (count >= 2)
                {
                    index = random.Next(queryAnswer.Count);
                    option = queryAnswer[index];
                    questionToReturn.Options.Add("option" + (optionIndex++).ToString(), option);
                }
                else
                {   
                    character = GetRandomCharacter(characterList);
                    queryAnswer = GetQueryAnswer(question.Query, character);
                    foreach (var value in questionToReturn.Options.Values) //*
                    {
                        if (queryAnswer.Contains(value))
                            queryAnswer.Remove(value);
                    }

                    while (queryAnswer.Count == 0)
                    {
                        character = GetRandomCharacter(characterList);
                        queryAnswer = GetQueryAnswer(question.Query, character);
                        foreach (var value in questionToReturn.Options.Values) //*
                        {
                            if (queryAnswer.Contains(value))
                                queryAnswer.Remove(value);
                        }
                        characterList.Remove(character);
                    }
                    index = random.Next(queryAnswer.Count);
                    option = queryAnswer[index];
                    questionToReturn.Options.Add("option" + (optionIndex++).ToString(), option);
                    characterList.Remove(character);
                }
                character = GetRandomCharacter(characterList);
                queryAnswer = GetQueryAnswer(question.Query, character);
                foreach (var value in questionToReturn.Options.Values) //*
                {
                    if (queryAnswer.Contains(value))
                        queryAnswer.Remove(value);
                }
                while (queryAnswer.Count == 0)
                {
                    character = GetRandomCharacter(characterList);
                    queryAnswer = GetQueryAnswer(question.Query, character);
                    foreach (var value in questionToReturn.Options.Values) //*
                    {
                        if (queryAnswer.Contains(value))
                            queryAnswer.Remove(value);
                    }
                    characterList.Remove(character);
                }
                index = random.Next(queryAnswer.Count);
                option = queryAnswer[index];
                questionToReturn.Options.Add("option" + (optionIndex++).ToString(), option );
            }

            return questionToReturn;
        }

        public List<QuestionToReturn> GetQuestions(List<string> characters, int nrOfQuestions)
        {
            List<QuestionToReturn> questionsToReturn = new List<QuestionToReturn>();

            for (int i = 0; i < nrOfQuestions; i++)
            {
                var selectedCharacter = GetRandomCharacter(characters);
                var question = GetRandomQuestion(selectedCharacter);
                questionsToReturn.Add(question);
                characters.Remove(selectedCharacter);
            }
            return questionsToReturn;
        }

        private string GetCharacterAvatar(string characterName, string characterUniverse)
        {
            SparqlParameterizedString queryString = new SparqlParameterizedString();

            queryString.Namespaces.AddNamespace("foaf", new Uri("http://xmlns.com/foaf/0.1/"));
            queryString.Namespaces.AddNamespace("rdfs", new Uri("http://www.w3.org/2000/01/rdf-schema#"));

            queryString.CommandText = "SELECT ?image WHERE { ?subject foaf:member ?universe; rdfs:label @name; foaf:img ?image. ?universe rdfs:label @universe } LiMIT 1";
            queryString.SetLiteral("name", characterName);
            queryString.SetLiteral("universe", characterUniverse);

            SparqlQueryParser parser = new SparqlQueryParser();
            SparqlQuery query = parser.ParseFromString(queryString);

            SparqlRemoteEndpoint endpoint = new SparqlRemoteEndpoint(new Uri(SparqlEndPoint.TripleStore));
            SparqlResultSet results = endpoint.QueryWithResultSet(query.ToString());

            var result = results.First()[0].ToString();

            return result;
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

            SparqlRemoteEndpoint endpoint = new SparqlRemoteEndpoint(new Uri("http://localhost:3030/gada_set/query"));
            SparqlResultSet results = endpoint.QueryWithResultSet(query.ToString());

            characterList = results.Select(x => x[0].ToString()).ToList();  

            return characterList;
        }

        public Answer CheckAnswer(Answer answer)
        {

            string questionTemplate = "";

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

                var queryResult = GetQueryAnswer(query, answer.Subject);

                foreach(var option in answer.Options)
                {
                    if ((queryResult.Contains(option.Value) && option.Checked == true) ||
                            (!queryResult.Contains(option.Value) && option.Checked == false))
                    {
                        var optionIndex = answer.Options.FindIndex(o => o == option);
                        answer.Options[optionIndex].IsCorrect = true;
                    }
                }
            }
            return answer;
        }

    }
}
