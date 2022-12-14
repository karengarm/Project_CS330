# coding=utf-8
""" Fine-tuning GPT2 on a intermediate tasks.
Author: Karen Garcia"""

import argparse
from transformers import TextDataset, DataCollatorForLanguageModeling
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from transformers import Trainer, TrainingArguments


def load_dataset(file_path, tokenizer, block_size=128):
    dataset = TextDataset(
        tokenizer=tokenizer,
        file_path=file_path,
        block_size=block_size,
    )
    return dataset


def load_data_collator(tokenizer, mlm=False):
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=mlm,
    )
    return data_collator


def train(model,
          tokenizer,
          data_collator,
          train_dataset,
          output_dir='/out',
          overwrite_output_dir=True,
          per_device_train_batch_size=8,
          num_train_epochs=1,
          max_steps=5,
          save_total_limit=1):
    training_args = TrainingArguments(
        output_dir=output_dir,
        overwrite_output_dir=overwrite_output_dir,
        per_device_train_batch_size=per_device_train_batch_size,
        num_train_epochs=num_train_epochs,
        max_steps=max_steps,
        save_total_limit=save_total_limit
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=train_dataset,
    )

    trainer.train()
    return model


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--train_file_path", default='src/squad.json', type=str,
                        help="Path to intermediate source task or target task data set.")
    parser.add_argument("--output_dir", default='/out', type=str,
                        help="The output directory where the model predictions and checkpoints will be written.")
    parser.add_argument("--model_name", default='gpt2', type=str,
                        help="Pretrained model name or directory")
    parser.add_argument('--overwrite_output_dir', default=True,
                        help="Overwrite the content of the output directory")
    parser.add_argument('--per_device_train_batch_size', default=8, type=int,
                        help="Batch size per GPU/CPU for training")
    parser.add_argument("--num_train_epochs", default=1, type=int,
                        help="Total number of training epochs to perform.")
    parser.add_argument("--max_steps", default=5, type=int,
                        help="Total number of training steps to perform.")
    parser.add_argument("--save_total_limit", default=1, type=int,
                        help="Steps to save.")

    args = parser.parse_args()

    tokenizer = GPT2Tokenizer.from_pretrained(args.model_name)
    train_dataset = load_dataset(args.train_file_path, tokenizer)
    data_collator = load_data_collator(tokenizer)
    model = GPT2LMHeadModel.from_pretrained(args.model_name)
    train(
        model,
        tokenizer,
        data_collator,
        train_dataset,
        output_dir=args.output_dir,
        overwrite_output_dir=args.overwrite_output_dir,
        per_device_train_batch_size=args.per_device_train_batch_size,
        num_train_epochs=args.num_train_epochs,
        max_steps=args.max_steps,
        save_total_limit=args.save_total_limit
    )


if __name__ == "__main__":
    main()