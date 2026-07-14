
#let data = json(bytes(sys.inputs.resume_data))

#set page(paper: "us-letter", margin: (x: 0.5in, y: 0.5in))
#set text(font: ("Helvetica Neue", "Arial", "sans-serif"), size: 9.5pt, fill: rgb("#333333"))
#set par(leading: 0.4em)
#set list(indent: 1em, body-indent: 0.5em, tight: true)

#show heading.where(level: 1): it => block(width: 100%, above: 0em, below: 0.5em)[
  #set align(center)
  #set text(size: 20pt, weight: "bold", fill: rgb("#2c3e50"))
  #it.body
]

#show heading.where(level: 2): it => block(width: 100%, above: 1.2em, below: 0.6em)[
  #set text(size: 12pt, weight: "bold", fill: rgb("#2c3e50"))
  #it.body
  #v(-0.4em)
  #line(length: 100%, stroke: 0.5pt + rgb("#bdc3c7"))
]

= #data.name

#align(center)[
  #text(size: 9.5pt, fill: rgb("#555555"))[
    #data.location | #data.title | #data.contact
  ]
]

#if data.sections.education.keep [
  == #data.sections.education.title
  #for edu in data.education [
    #block(width: 100%, breakable: false, above: 0.6em, below: 0.6em)[
      #grid(
        columns: (1fr, auto),
        gutter: 1em,
        [#text(weight: "bold")[#edu.school]],
        [#text(style: "italic", fill: rgb("#555555"))[#edu.date]]
      )
      #v(-0.4em)
      #text()[#edu.degree]
    ]
  ]
]

#if data.sections.skills.keep [
  == #data.sections.skills.title
  #block(width: 100%, breakable: false, above: 0.6em, below: 0.6em)[
    #for skill in data.skills [
      - *#skill.category:* #skill.details
    ]
  ]
]

#if data.sections.experience.keep [
  == #data.sections.experience.title
  #for job in data.experience [
    #block(width: 100%, breakable: false, above: 0.6em, below: 0.6em)[
      #grid(
        columns: (1fr, auto),
        gutter: 1em,
        [#text(weight: "bold")[#job.title | #job.company]],
        [#text(style: "italic", fill: rgb("#555555"))[#job.date]]
      )
      #if job.bullets.len() > 0 [
        #list(..job.bullets.map(b => [#b]))
      ]
    ]
  ]
]

#if data.sections.projects.keep [
  == #data.sections.projects.title
  #for proj in data.projects [
    #block(width: 100%, breakable: false, above: 0.6em, below: 0.6em)[
      #text(weight: "bold")[#proj.title]
      #if proj.subtitle != "" [ - #text(style: "italic")[#proj.subtitle] ]
      #if proj.bullets.len() > 0 [
        #list(..proj.bullets.map(b => [#b]))
      ]
    ]
  ]
]
