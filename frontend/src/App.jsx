import React, { useState, useEffect } from "react";
import axios from "axios";

const API_URL = "http://localhost:8000";

function App() {
  const [step, setStep] = useState(0); // 0: topic, 1: game
  const [topics, setTopics] = useState([]);
  const [selectedTopic, setSelectedTopic] = useState(null);
  const [sentence, setSentence] = useState("");
  const [choices, setChoices] = useState([]);
  const [answer, setAnswer] = useState("");
  const [hint, setHint] = useState("");
  const [userAnswer, setUserAnswer] = useState("");
  const [score, setScore] = useState(0);
  const [attempted, setAttempted] = useState(0);
  const [feedback, setFeedback] = useState("");
  const [showHint, setShowHint] = useState(false);

  useEffect(() => {
    axios.get(`${API_URL}/topics`).then((res) => setTopics(res.data));
  }, []);

  const startGame = (topic) => {
    setSelectedTopic(topic);
    setStep(1);
    fetchQuestion(topic.id);
    setScore(0);
    setAttempted(0);
    setFeedback("");
    setUserAnswer("");
    setShowHint(false);
  };

  const fetchQuestion = async (topic_id) => {
    setSentence("Loading...");
    setHint("");
    setChoices([]);
    setShowHint(false);
    const res = await axios.post(`${API_URL}/get_question`, { topic_id });
    setSentence(res.data.sentence);
    setChoices(res.data.choices.split(", "));
    setAnswer(res.data.answer);
    setHint(res.data.hint);
    setUserAnswer("");
    setFeedback("");
  };

  const submit = async () => {
    const res = await axios.post(`${API_URL}/submit_answer`, {
      topic_id: selectedTopic.id,
      sentence,
      choices: choices.join(", "),
      answer,
      hint,
      user_answer: userAnswer,
    });
    setAttempted((a) => a + 1);
    if (res.data.correct) {
      setScore((s) => s + 1);
      setFeedback("✅ Correct!");
    } else {
      setFeedback(`❌ Incorrect! The answer was: ${answer}`);
    }
    setTimeout(() => {
      fetchQuestion(selectedTopic.id);
    }, 1500);
  };

  if (step === 0) {
    return (
      <div style={{padding: 32}}>
        <h2>Select a Topic</h2>
        <ul>
          {topics.map((t) => (
            <li key={t.id}>
              <button onClick={() => startGame(t)}>{t.name}</button>
            </li>
          ))}
        </ul>
      </div>
    );
  }

  if (step === 1) {
    return (
      <div style={{padding: 32, maxWidth: 600, margin: "0 auto"}}>
        <h3>Topic: {selectedTopic.name}</h3>
        <div style={{marginBottom: 16}}>Score: {score} / {attempted}</div>
        <div style={{fontSize: 20, marginBottom: 16}}>{sentence}</div>
        <ul>
          {choices.map((c, i) => (
            <li key={i}>{c}</li>
          ))}
        </ul>
        <input
          value={userAnswer}
          onChange={e => setUserAnswer(e.target.value)}
          placeholder="Fill in the blank"
          style={{fontSize: 18, padding: 4}}
          onKeyDown={e => e.key === 'Enter' && submit()}
        />
        <button onClick={submit} style={{marginLeft: 8}}>Submit</button>
        <button onClick={() => setShowHint(true)} style={{marginLeft: 8}}>Show Hint</button>
        {showHint && <div style={{marginTop: 10, fontStyle: "italic"}}>Hint: {hint}</div>}
        <div style={{marginTop: 16}}>{feedback}</div>
        <button style={{marginTop: 24}} onClick={() => setStep(0)}>Change Topic</button>
      </div>
    );
  }

  return <div>Unknown step.</div>;
}

export default App;
