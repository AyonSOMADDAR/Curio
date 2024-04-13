**CURIO: Learn your way, At your pace.** 

**Problem Statement:** 

**PS-ID:** GAPS-07 

**Problem Statement Title:** Analysis on ChatGPT. 

**Objec ve:**  Your  task  is  to  create  a  genera ve  AI-powered  applica on  using OpenAI() API that dynamically generates personalized educa onal content. This content  should  not  only  align  with  the  curriculum  but  also  adapt  to  each student's learning progress, areas of interest, and preferred learning modali es (text, visual, etc.). 

**Deliverables:**  

- A fully func onal prototype that integrates Gemini Pro's API for real- me, personalized content genera on. 
- Documenta on  detailing  the  system  architecture,  Gemini  Pro  API integra on, personaliza on logic, and user interface design. 
- A  presenta on  that  demonstrates  the  applica on's  func onality, highlights  its  innova ve  features,  and  discusses  poten al  impacts  on personalized e-learning. 

**Proposed System:** 

We  propose  **“Curio”**,  an  innova ve  AI-Powered  applica on  u lizing  **Large Language  Models(LLM)**  like  **Gemini  Pro**  to  reshape  personalized  E-learning. Integra ng advanced **Natural Language Processing (NLP)** harnessing the power of **Langchain** framework, Curio dynamically and seman cally searches through the educa onal content of the students and answers promptly. As an adap ve applica on, Curio answers as per student’s individual details and personalizes itself as per students learning capabili es.  By tapping into **Gemini Pro's API**, it generates real- me, curriculum-aligned materials that adapt to each student's interests, and preferred learning styles. In addi on to these,Curio implements **Reinforcement  Learning  with  Human  Feedback  (RLHF),**  enhancing  learning outcomes by itera vely refining content based on user input for the feedback using a **Reward Model** and **Proximal Policy Op miza on (PPO)** . With a user- friendly  interface  and  scalable  architecture,  Curio  promises  to  revolu onize educa onal experiences, making personalized learning accessible and effec ve for students worldwide. 

**Architecture:** 

Our basic architectural implementa on involves a Langchain framework implemen ng the Gemini Pro by Google as a large language model, Faiss by Meta as a vectorstore and other fine tuning methodologies to implement personalisa on and achieve be er results. 

Here is the architectural framework: 

![](Aspose.Words.ce81b54e-1a07-4ff2-a993-688ff6fbd6a2.002.jpeg)

As men oned in the image above, we u lize extensive finetuning techniques like **Reinforcement Learning Human Feedback system, quiz based analysis** and **individual informa on** for personaliza on. Inputs taken by the bot ini ally to uniquely iden fy: 

![](Aspose.Words.ce81b54e-1a07-4ff2-a993-688ff6fbd6a2.003.png)

**Personaliza on architecture** along with implementa on design: 

1. **Profile Playground:** 
- The bot takes survey about the student and fine tunes itself as per the input received.**  
- The model fetches the answers accordingly and generates result. 
- We have named this sec on as the **“Profile Playground”.** It generates survey ques on to enquire about demographics, learning history, and other useful data.** 

![](Aspose.Words.ce81b54e-1a07-4ff2-a993-688ff6fbd6a2.004.jpeg)

2. **Quizzie:** 

   It helps the bot to understand the users domain knowledge. It generates ques on for the user and allows the user to answer that ques on. The reply of the user helps bot to learn about users knowledge depth. 

![](Aspose.Words.ce81b54e-1a07-4ff2-a993-688ff6fbd6a2.005.jpeg)

3. **Regenerate Op ons: **

   This helps to take user feedback from the users about the produced data. 

![](Aspose.Words.ce81b54e-1a07-4ff2-a993-688ff6fbd6a2.006.jpeg)

4. **Document and Image Parsing:** 

   This allows the user to interact with an image or a document and ask ques ons related to it. 

Project GitHub Link:[ h ps://github.com/AyonSOMADDAR/Curio  ](https://github.com/AyonSOMADDAR/Curio)![ref1]![](Aspose.Words.ce81b54e-1a07-4ff2-a993-688ff6fbd6a2.007.jpeg)

[ref1]: Aspose.Words.ce81b54e-1a07-4ff2-a993-688ff6fbd6a2.001.jpeg
