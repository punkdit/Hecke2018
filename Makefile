
all: algebraic.pdf sketches.pdf


algebraic.pdf: algebraic.tex   dynkin.tex
	pdflatex algebraic.tex
	bibtex algebraic
	pdflatex algebraic.tex
	pdflatex algebraic.tex

dolan.pdf: dolan.tex  refs2.bib
	pdflatex dolan.tex
	bibtex dolan
	pdflatex dolan.tex
	pdflatex dolan.tex


sketches.pdf: sketches.tex  refs2.bib
	pdflatex sketches.tex
	bibtex sketches
	pdflatex sketches.tex
	pdflatex sketches.tex


hecke.pdf: hecke.tex  refs.bib
	pdflatex hecke.tex
	bibtex hecke
	pdflatex hecke.tex
	pdflatex hecke.tex


