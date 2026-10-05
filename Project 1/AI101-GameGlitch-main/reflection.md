# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

The Hints were backwards.
You can see the answer in the developer debug information.
When hitting the button to restart the game wont restart
Runs out of attemps 1 too early
Im not too sure that the scoring is working as intended.
Cannot click enter to input the wanted value
No confirmation if something is wrong. 

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
 enter      input to go in    nothing happens   NA
 55      go higher             go lower         NA
60       go lower            go higher         NA

---

## 2. How did you use AI as a teammate?
I gave AI a list of things that were bugs or that I considered to be bugs in the code provided. I asked AI to give me a list of other things that it could find that might be logic not working as intended. 

-used claude
-secret number changing when changing dificulty. I wasnt able to catch that but claude was
-it wanted to make the harder versions "harder" by increasing the range of numbers


- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

---

## 3. Debugging and testing your fixes
I decided if a bug was fixed by testing it out once more
-
-Claude aided in writting test cases, I would let it know what sort of test I was wanting to run and it would check them. 

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

Learnt that streamlit is actually super usefull to create things that need to be operated on a dashboard. z
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

-I want to preserve the way that I utilized AI to help me not finish for me
-I would want to review the code AI is writting more. I am currently using AI on my powershell so its hard to see the changes that its performing
-I can see that it can be wrong and that we shouldnt follow blindly. More of a tool to aid rather than do.

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
