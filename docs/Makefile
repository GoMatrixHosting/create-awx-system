all: User_Manual.pdf User_Manual.md
	@true

User_Manual.md: User_Manual.odt
	pandoc $< -o ./generated/$@

User_Manual.pdf: User_Manual.odt
	pandoc $< -o ./generated/$@

install-deps:
	sudo apt install pandoc texlive-extra-utils
