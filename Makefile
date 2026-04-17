DICT_NAME		=	"Gabra"
DICT_SRC		=	Gabra.xml
DICT_BUILD_TOOL_DIR	=	"/Applications/Dictionary Development Kit"
DICT_BUILD_TOOL_BIN	=	$(DICT_BUILD_TOOL_DIR)/bin

###########################

DICT_DEV_KIT_OBJ_DIR	=	./objects
export	DICT_DEV_KIT_OBJ_DIR

DESTINATION_FOLDER	=	~/Library/Dictionaries
rm			=	/bin/rm

###########################

all:
	$(DICT_BUILD_TOOL_BIN)/build_dict.sh $(DICT_NAME) $(DICT_SRC) MyDict.css MyInfo.plist
	echo "Done."

install:
	echo "Installing..."
	mkdir -p $(DESTINATION_FOLDER)
	cp -r $(DICT_DEV_KIT_OBJ_DIR)/$(DICT_NAME).dictionary $(DESTINATION_FOLDER)
	touch $(DESTINATION_FOLDER)
	echo "Done."

clean:
	$(rm) -rf $(DICT_DEV_KIT_OBJ_DIR)
