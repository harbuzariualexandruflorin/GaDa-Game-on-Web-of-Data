namespace QuizAPI.Core
{
    public enum Type { Marvel, Pokemon, StarWars, StarTrek};

    public class Question
    {
        public string QuizQuestion { get; set; }

        //public Type QuestionType { get; set; }

        public string QuestionType { get; set; }

        public bool MultipleChoice { get; set; }

        public string Query { get; set; }
    }
}
