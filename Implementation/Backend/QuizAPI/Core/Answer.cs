namespace QuizAPI.Core
{
    public class Answer
    {
        public string Question { get; set; }

        public string Subject { get; set; }

        public List<string> QuestionAnswer { get; set; }
    }
}
