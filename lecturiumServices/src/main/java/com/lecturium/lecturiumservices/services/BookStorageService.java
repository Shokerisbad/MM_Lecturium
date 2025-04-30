package com.lecturium.lecturiumservices.services;

import com.lecturium.lecturiumservices.models.LoadFile;
import com.mongodb.BasicDBObject;
import com.mongodb.DBObject;
import com.mongodb.client.gridfs.model.GridFSFile;
import org.apache.commons.io.IOUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.data.mongodb.gridfs.GridFsOperations;
import org.springframework.data.mongodb.gridfs.GridFsTemplate;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;


@Service
public class BookStorageService {

    @Autowired
    private GridFsTemplate template;

    @Autowired
    private GridFsOperations operations;

    public String uploadFile(MultipartFile file) throws IOException {

        DBObject metadata = new BasicDBObject();
        metadata.put("filesize", file.getSize());

        Object fileId = template.store(file.getInputStream(),file.getOriginalFilename(),file.getContentType(),metadata);

        return fileId.toString();
    }

    public LoadFile downloadFile(String fileId) throws IOException {
        GridFSFile gridFSFile = template.findOne(Query.query(Criteria.where("_id").is(fileId)));
        LoadFile loadFile = new LoadFile();

        if(gridFSFile != null && gridFSFile.getMetadata() != null){
            loadFile.setFilename((gridFSFile.getFilename()));
            loadFile.setFileType( gridFSFile.getMetadata().get("_contentType").toString() );

            loadFile.setFileSize( gridFSFile.getMetadata().get("fileSize").toString() );

            loadFile.setFile( IOUtils.toByteArray(operations.getResource(gridFSFile).getInputStream()) );
        }

        return loadFile;
    }

}
