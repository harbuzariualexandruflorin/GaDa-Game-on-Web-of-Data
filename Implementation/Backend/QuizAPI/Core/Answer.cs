namespace QuizAPI.Core
{
    public class Answer
    {
        public string Question { get; set; }

        public string Subject { get; set; }

        //public List<string> QuestionAnswer { get; set; }
        public List<Option> Options { get; set; }

        public Answer(string question, string subject, List<Option> options)
        {
            Question = question;
            Subject = subject;
            Options = options;
        }
    }
}
