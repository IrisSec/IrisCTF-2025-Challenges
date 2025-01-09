#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>
#include <string.h>

typedef struct {
    char* fileName;
    int fileSize;
    unsigned long long hash;
    int dataOffset;
} FileMetadata;

typedef struct {
    int zipLength;
    unsigned char zipData[0x200];
} FileData;

typedef struct {
    char* name;
    char* pass;
    int isAdmin;
    int dataCount;
    FileData datas[256];
} FileUser;

#pragma pack(push)
#pragma pack(1)
typedef struct {
    uint32_t magic;
    uint16_t version;
    uint16_t generalPurposeBitFlag;
    uint16_t compressionType;
    uint32_t lastModified;
    uint32_t checksum;
    uint32_t compressedSize;
    uint32_t uncompressedSize;
} ZipFileHeader;
#pragma pack(pop)

FileUser fileUsers[16];

unsigned long long hash(unsigned char* str, int length) {
    unsigned long long hash = 0xcbf29ce484222325UL;
    int i = 0;
    while (i < length) {
        //printf("hashing byte %02x\n", str[i]);
        hash ^= str[i++];
        hash *= 0x00000100000001B3UL;
    }

    return hash;
}

int readFile(unsigned char* out, char* name, int maxlen) {
    FILE* f = fopen(name, "rb");
    if (f == NULL) {
        return -1;
    }

    fseek(f, 0, SEEK_END);
    long len = ftell(f);
    fseek(f, 0, SEEK_SET);

    if (len > maxlen) {
        len = maxlen;
    }

    size_t read = fread(out, 1, len, f);
    fclose(f);
    return read == len ? read : -1;
}

int readHex(unsigned char* out, char* inp, int inplen) {
    int outi = 0;
    for (int i = 0; i < inplen;) {
        char c1 = inp[i++];
        if (c1 == ' ') {
            continue;
        }
        if (!isxdigit(c1)) {
            return -1;
        }

        if (i >= inplen) {
            return -1;
        }
        char c2 = inp[i++];
        if (!isxdigit(c2)) {
            return -1;
        }

        out[outi++] = (
            ((isdigit(c1) ? c1 - '0' : toupper(c1) - 'A' + 10) << 4) |
            (isdigit(c2) ? c2 - '0' : toupper(c2) - 'A' + 10)
        );
    }

    return outi;
}

bool readZipInfo(FileMetadata* fileMeta, unsigned char* data, int length) {
    ZipFileHeader* zipFileHeader = (ZipFileHeader*)data;
    void* zipAfterHeader = zipFileHeader + 1;
    
    if (zipFileHeader->magic != 0x04034b50) {
        printf("ZIP magic expected\n");
        return false;
    }

    if (zipFileHeader->compressionType != 0) {
        printf("Only uncompressed files are supported\n");
        return false;
    }

    int fileNameAndExtraLength = *(int*)zipAfterHeader;
    if ((short)fileNameAndExtraLength != fileNameAndExtraLength) {
        printf("Extra field not supported\n");
        return false;
    }
    
    short fileNameLength = (short)fileNameAndExtraLength;
    if (fileNameLength > length - (int)sizeof(ZipFileHeader)) {
        printf("File name length too long (assert %d > %d)\n", fileNameLength, length - sizeof(ZipFileHeader));
        return false;
    }

    fileMeta->fileName = calloc(1, 0x200);
    for (int i = 0; i < fileNameLength; i++) {
        fileMeta->fileName[i] = *((char*)zipAfterHeader + 4 + i);
    }

    if (zipFileHeader->compressedSize > length - sizeof(ZipFileHeader) - 4 - fileNameLength) {
        printf("File data length too long\n");
        return false;
    }

    /*if (zipFileHeader->compressedSize > 0x200) {
        printf("File data length longer than 0x200, trimming\n");
        zipFileHeader->compressedSize = 0x200;
    } else*/ if (zipFileHeader->compressedSize < 10) {
        printf("There is no reason to upload a file this small :(\n");
        return false;
    }

    fileMeta->fileSize = zipFileHeader->compressedSize;
    fileMeta->dataOffset = sizeof(ZipFileHeader) + 4 + fileNameLength;
    fileMeta->hash = hash((char*)zipAfterHeader + 4 + fileNameLength, zipFileHeader->compressedSize);

    // ignore the rest of the zip
    return true;
}

void setupUsers() {
    for (int i = 0; i < 16; i++) {
        FileUser* emptyUser = &fileUsers[i];
        emptyUser->name = NULL;
        emptyUser->pass = NULL;
        emptyUser->dataCount = 0;
    }

    for (int i = 0; i < 16; i++) {
        for (int j = 0; j < 256; j++) {
            fileUsers[i].datas[j].zipLength = -1;
        }
    }
    
    // add tom stuff
    
    FILE* urand = fopen("/dev/urandom", "r");
    if (urand == NULL) {
        exit(1);
    }

    unsigned char randBuf[63];
    fread(randBuf, 63, 1, urand);
    
    char tomPass[64]; tomPass[63] = -1;
    for (int i = 0; i < 63; i++) {
        tomPass[i] = '0' + (randBuf[i] % 10);
    }
    fclose(urand);
    
    // char tomPass[64]; // should be random
    // strcpy(tomPass, "test");

    FileUser* tomUser = &fileUsers[15];
    tomUser->name = "Tom";
    tomUser->pass = strdup(tomPass);
    tomUser->isAdmin = 1;
    tomUser->dataCount = 1;
    
    FileData* tomFirstData = &tomUser->datas[0];
    int invCodeLen = readFile(tomFirstData->zipData, "invite.zip", sizeof(tomFirstData->zipData));
    tomFirstData->zipLength = invCodeLen;
}

void listUsers() {
    for (int i = 0; i < 16; i++) {
        FileUser* user = &fileUsers[i];
        if (user->name != NULL) {
            printf("[UID=%d] %s\n", i, user->name);
        }
    }
}

void listFiles() {
    int id;
    printf("For which user id? ");
    if (scanf("%d", &id) != 1 || id < 0 || id > 15 || fileUsers[id].name == NULL) {
        printf("Bad user id\n");
        return;
    }
    
    FileUser* user = &fileUsers[id];
    for (int i = 0; i < user->dataCount; i++) {
        FileData* fileData = &user->datas[i];
        if (fileData->zipLength > -1) {
            FileMetadata metadata;
            bool valid = readZipInfo(&metadata, fileData->zipData, fileData->zipLength);
            if (valid) {
                printf("[FID=%d] %s %d %llx\n", i, metadata.fileName, metadata.fileSize, metadata.hash);
            }
        }
    }
}

bool checkInvite(char* inviteStr) {
    FileMetadata metadata;
    FileData* data = &fileUsers[15].datas[0];
    bool valid = readZipInfo(&metadata, data->zipData, data->zipLength);
    if (!valid) {
        printf("Invalid zip\n");
        return false;
    }

    unsigned char* bufferPtr = data->zipData + metadata.dataOffset;

    //printf("compare %s == %s\n", bufferPtr, inviteStr);
    return memcmp(bufferPtr, inviteStr, metadata.fileSize) == 0;
}

void createUser() {
    for (int i = 0; i < 16; i++) {
        FileUser* user = &fileUsers[i];
        if (user->name == NULL) {
            char inviteTmp[50]; inviteTmp[49] = '\0';
            char usernameTmp[50]; usernameTmp[49] = '\0';
            char passwordTmp[50]; passwordTmp[49] = '\0';

            printf("Invite code? ");
            scanf("%49s", inviteTmp);
            if (!checkInvite(inviteTmp)) {
                printf("Invalid invite code\n");
                return;
            }

            printf("Username? ");
            scanf("%49s", usernameTmp);
            user->name = strdup(usernameTmp);

            printf("Password? ");
            scanf("%49s", passwordTmp);
            user->pass = strdup(passwordTmp);

            printf("[UID=%d] %s\n", i, user->name);
            return;
        }
    }

    printf("Max number of users already created\n");
}

void uploadFile() {
    int id;
    printf("Which user id do you want to upload this file to? ");
    if (scanf("%d", &id) != 1 || id < 0 || id > 15 || fileUsers[id].name == NULL) {
        printf("Bad user id\n");
        return;
    }

    FileUser* user = &fileUsers[id];
    int nextFileId = user->dataCount;
    if (nextFileId >= 256) {
        printf("Max number of files already created\n");
        return;
    }

    FileData* data = &user->datas[nextFileId];

    char hexTmp[1024]; hexTmp[1023] = '\0';
    printf("Paste the hex of a zip file (less than 512 bytes)\n");
    printf("The zip file must only contain one uncompressed file\n");
    scanf("%1023s", hexTmp);

    int dataLen = readHex(data->zipData, hexTmp, strlen(hexTmp));
    if (dataLen < 0) {
        printf("Invalid hex\n");
        return;
    }

    data->zipLength = dataLen;
    
    FileMetadata metadata;
    bool valid = readZipInfo(&metadata, data->zipData, data->zipLength);
    if (!valid) {
        printf("Invalid zip\n");
        return;
    }

    user->dataCount++;
    printf("File created\n");
}

FileUser* askUserAndPass() {
    int id;
    printf("User id? ");
    if (scanf("%d", &id) != 1 || id < 0 || id > 15 || fileUsers[id].name == NULL) {
        printf("Bad user id\n");
        return NULL;
    }

    FileUser* user = &fileUsers[id];
    char passwordTmp[50]; passwordTmp[49] = '\0';

    printf("Password? ");
    scanf("%49s", passwordTmp);
    if (strcmp(user->pass, passwordTmp) != 0) {
        printf("Incorrect password\n");
        return NULL;
    }

    return user;
}

void viewFile() {
    FileUser* user = askUserAndPass();
    if (user == NULL) {
        return;
    }

    int fid;
    printf("Which file id do you want to contents of? ");
    if (scanf("%d", &fid) != 1 || fid < 0 || fid > 255 || user->datas[fid].zipLength == -1) {
        printf("Bad file id\n");
        return;
    }

    FileMetadata metadata;
    FileData* data = &user->datas[fid];
    bool valid = readZipInfo(&metadata, data->zipData, data->zipLength);
    if (!valid) {
        printf("Invalid zip\n");
        return;
    }

    // zip max size is 0x200, so inner file size has to be less than 0x200
    char fileBuffer[0x200];
    int fileSize = metadata.fileSize;
    if (fileSize >= sizeof(fileBuffer) - 1) {
        fileSize = sizeof(fileBuffer) - 1;
    }

    memcpy(fileBuffer, data->zipData + metadata.dataOffset, fileSize);
    fileBuffer[fileSize] = '\0';

    printf(fileBuffer);
}

void viewFlag() {
    FileUser* user = askUserAndPass();
    if (user == NULL) {
        return;
    }

    if (user->isAdmin != 0) {
        char flagText[128];
        int flagLen = readFile(flagText, "flag.txt", 127);
        flagText[flagLen] = '\0';
        printf("Flag: %s\n", flagText);
    } else {
        printf("Not admin.\n");
    }
}

int main(int argc, const char* argv[]) {
	setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
	
    setupUsers();
    printf("Welcome to MyFiles 2K, where we store your files as secure ZIPs.\n");
    while (true) {
        printf("1. List users\n");
        printf("2. List files\n");
        printf("3. Create user\n");
        printf("4. Upload file\n");
        printf("5. View file\n");
        printf("6. Get flag\n");
        printf("7. Exit\n");

        int choice;
        printf("> ");
        if (scanf("%d", &choice) != 1 || choice < 1 || choice > 7) {
            printf("Bad choice\n");
            getchar();
            continue;
        }

        printf("\n");
        if (choice == 1) {
            listUsers();
        } else if (choice == 2) {
            listFiles();
        } else if (choice == 3) {
            createUser();
        } else if (choice == 4) {
            uploadFile();
        } else if (choice == 5) {
            viewFile();
        } else if (choice == 6) {
            viewFlag();
        } else if (choice == 7) {
            break;
        }
        printf("\n");
    }

    printf("Bye\n");
    return 0;
}