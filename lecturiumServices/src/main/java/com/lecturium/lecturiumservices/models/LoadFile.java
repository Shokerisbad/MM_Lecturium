package com.lecturium.lecturiumservices.models;

import lombok.Getter;
import lombok.Setter;

@Setter
@Getter
public class LoadFile {

    private String filename;
    private String fileType;
    private String fileSize;
    private byte[] file;

    public LoadFile() {
    }

}